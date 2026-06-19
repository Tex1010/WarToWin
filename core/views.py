import re
import secrets

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    AdminUserAccountForm,
    LeaderForm,
    MatchRequestForm,
    MemberForm,
    UsernameUpdateForm,
    RecruitmentForm,
    RuleForm,
    TeamSettingsForm,
)
from .models import (
    Leader,
    MatchRequest,
    Member,
    RecruitmentApplication,
    Rule,
)
from .utils import get_team_settings


User = get_user_model()


def _sanitize_username(value: str) -> str:
    value = (value or "").strip().replace(" ", "_")
    value = re.sub(r"[^\w.@+-]+", "", value, flags=re.UNICODE)
    return value[:150]


def _available_username(base: str) -> str:
    base = _sanitize_username(base)
    if not base:
        base = "member"

    candidate = base
    idx = 2
    while User.objects.filter(username__iexact=candidate).exists():
        suffix = str(idx)
        candidate = f"{base[:150 - len(suffix)]}{suffix}"
        idx += 1
    return candidate


def _ensure_member_account(member: Member):
    if member.user_id:
        return member.user, None, False

    username = _available_username(member.pseudo or member.name or "member")
    password = secrets.token_urlsafe(9)
    user = User.objects.create_user(username=username, password=password)
    member.user = user
    member.save(update_fields=["user"])
    return user, password, True


def _apply_bootstrap_classes(form):
    for field in form.fields.values():
        input_type = getattr(field.widget, "input_type", "")
        existing = field.widget.attrs.get("class", "")
        if input_type == "checkbox":
            field.widget.attrs["class"] = (existing + " form-check-input").strip()
        else:
            field.widget.attrs["class"] = (existing + " form-control").strip()


class CustomLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        if self.request.user.is_staff:
            return "/admin-panel/"

        return "/account/"


def home(request):
    settings = get_team_settings()
    leaders = Leader.objects.all()
    members_count = Member.objects.count()
    match_form = MatchRequestForm(request.POST or None)

    if request.method == "POST" and request.POST.get("form_name") == "match_request":
        if match_form.is_valid():
            match_form.save()
            messages.success(
                request,
                "Ta demande de match a bien ete envoyee. L'admin la verifiera bientot.",
            )
            return redirect("home")

        messages.error(request, "Impossible d'envoyer la demande de match.")

    return render(
        request,
        "index.html",
        {
            "settings": settings,
            "leaders": leaders,
            "members_count": members_count,
            "match_form": match_form,
        },
    )


def members(request):
    context = {
        "leaders": Leader.objects.all(),
        "members": Member.objects.all(),
    }
    return render(request, "members.html", context)


def rules(request):
    return render(request, "rules.html", {"rules": Rule.objects.all()})


def recruitment(request):
    form = RecruitmentForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Ta candidature a bien ete envoyee. La team la verifiera bientot.",
        )
        return redirect("recruitment")

    return render(request, "recruitment.html", {"form": form})


def build_admin_context():
    team_settings = get_team_settings()
    pending_applications = RecruitmentApplication.objects.filter(
        status=RecruitmentApplication.STATUS_PENDING
    )
    reviewed_applications = RecruitmentApplication.objects.exclude(
        status=RecruitmentApplication.STATUS_PENDING
    )
    pending_match_requests = MatchRequest.objects.filter(
        status=MatchRequest.STATUS_PENDING
    )
    reviewed_match_requests = MatchRequest.objects.exclude(
        status=MatchRequest.STATUS_PENDING
    )

    return {
        "members": Member.objects.all(),
        "leaders": Leader.objects.all(),
        "rules": Rule.objects.all(),
        "leader_form": LeaderForm(),
        "rule_form": RuleForm(),
        "settings": team_settings,
        "settings_form": TeamSettingsForm(instance=team_settings),
        "pending_applications": pending_applications,
        "reviewed_applications": reviewed_applications,
        "applications_count": RecruitmentApplication.objects.count(),
        "pending_count": pending_applications.count(),
        "accepted_count": reviewed_applications.filter(
            status=RecruitmentApplication.STATUS_ACCEPTED
        ).count(),
        "rejected_count": reviewed_applications.filter(
            status=RecruitmentApplication.STATUS_REJECTED
        ).count(),
        "pending_match_requests": pending_match_requests,
        "reviewed_match_requests": reviewed_match_requests,
        "match_requests_count": MatchRequest.objects.count(),
        "pending_match_count": pending_match_requests.count(),
    }


@staff_member_required(login_url="/login/")
def admin_panel(request):
    return render(request, "admin_panel.html", build_admin_context())


@staff_member_required(login_url="/login/")
@require_POST
def update_team_settings(request):
    settings = get_team_settings()
    form = TeamSettingsForm(request.POST, request.FILES, instance=settings)

    if form.is_valid():
        form.save()
        messages.success(request, "Les informations du site ont ete mises a jour.")
    else:
        messages.error(request, "Impossible de mettre a jour les parametres du site.")

    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def add_member(request):
    form = MemberForm(request.POST, request.FILES)

    if form.is_valid():
        member = form.save()
        _, password, created = _ensure_member_account(member)
        if created:
            messages.success(
                request,
                f"Membre ajoute avec succes. Compte cree: {member.user.username} / {password}",
            )
        else:
            messages.success(request, "Membre ajoute avec succes.")
    else:
        messages.error(request, "Impossible d'ajouter le membre.")

    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
def add_leader(request):
    form = LeaderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Leader ajoute avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Ajouter un leader"})


@staff_member_required(login_url="/login/")
def add_rule(request):
    form = RuleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reglement ajoute avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Ajouter un reglement"})


@staff_member_required(login_url="/login/")
def edit_rule(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    form = RuleForm(request.POST or None, instance=rule)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reglement modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un reglement"})


@staff_member_required(login_url="/login/")
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, request.FILES or None, instance=member)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Membre modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un membre"})


@staff_member_required(login_url="/login/")
def edit_leader(request, pk):
    leader = get_object_or_404(Leader, pk=pk)
    form = LeaderForm(request.POST or None, request.FILES or None, instance=leader)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Leader modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un leader"})


@staff_member_required(login_url="/login/")
@require_POST
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    messages.success(request, "Membre supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def delete_leader(request, pk):
    leader = get_object_or_404(Leader, pk=pk)
    leader.delete()
    messages.success(request, "Leader supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def delete_rule(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    messages.success(request, "Reglement supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def delete_application(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    application.delete()
    messages.success(request, "Candidature supprimee de l'historique.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def accept_application(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    admin_note = request.POST.get("admin_note", "").strip()

    if application.status != RecruitmentApplication.STATUS_PENDING:
        messages.warning(request, "Cette candidature a deja ete traitee.")
        return redirect("admin_panel")

    if Member.objects.filter(pseudo__iexact=application.pseudo).exists():
        messages.error(
            request,
            "Ce pseudo existe deja parmi les membres. Verifie avant validation.",
        )
        return redirect("admin_panel")

    with transaction.atomic():
        member = Member.objects.create(
            name=application.full_name,
            pseudo=application.pseudo,
            photo=application.profile_photo,
            slogan=f"Niveau {application.get_level_display()}",
            ff_profile_photo=application.profile_screenshot,
        )
        _, password, _ = _ensure_member_account(member)
        application.status = RecruitmentApplication.STATUS_ACCEPTED
        application.admin_note = admin_note
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.save(update_fields=["status", "admin_note", "reviewed_at", "reviewed_by"])

    messages.success(
        request,
        f"Candidature acceptee, membre ajoute, compte cree: {member.user.username} / {password}",
    )
    return redirect("admin_panel")


@login_required(login_url="/login/")
def member_account(request):
    if request.user.is_staff:
        return redirect("admin_panel")

    member = Member.objects.filter(user=request.user).first()
    profile_form = MemberForm(instance=member) if member else None
    username_form = UsernameUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    _apply_bootstrap_classes(password_form)

    if request.method == "POST":
        form_name = request.POST.get("form_name")
        if form_name == "profile":
            if not member:
                messages.error(request, "Aucun profil membre n'est lie a ce compte.")
                return redirect("member_account")

            profile_form = MemberForm(request.POST, request.FILES, instance=member)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profil membre mis a jour.")
                return redirect("member_account")
        elif form_name == "username":
            username_form = UsernameUpdateForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Nom d'utilisateur mis a jour.")
                return redirect("member_account")
        elif form_name == "password":
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            _apply_bootstrap_classes(password_form)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Mot de passe mis a jour.")
                return redirect("member_account")
        else:
            messages.error(request, "Action inconnue.")

    return render(
        request,
        "member_account.html",
        {
            "member": member,
            "profile_form": profile_form,
            "username_form": username_form,
            "password_form": password_form,
        },
    )


@staff_member_required(login_url="/login/")
def user_accounts(request):
    members = Member.objects.select_related("user").order_by("pseudo")
    return render(request, "user_accounts.html", {"members": members})


@staff_member_required(login_url="/login/")
@require_POST
def create_member_account(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    _, password, created = _ensure_member_account(member)
    if created:
        messages.success(
            request,
            f"Compte cree pour {member.pseudo}: {member.user.username} / {password}",
        )
    else:
        messages.info(request, f"{member.pseudo} a deja un compte.")
    if "/admin-panel/" in request.META.get("HTTP_REFERER", ""):
        return redirect("admin_panel")
    return redirect("user_accounts")


@staff_member_required(login_url="/login/")
def user_account_edit(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if not member.user_id:
        messages.error(request, "Ce membre n'a pas encore de compte.")
        return redirect("user_accounts")

    account_form = AdminUserAccountForm(instance=member.user)
    password_form = SetPasswordForm(user=member.user)
    _apply_bootstrap_classes(password_form)

    if request.method == "POST":
        form_name = request.POST.get("form_name")
        if form_name == "account":
            account_form = AdminUserAccountForm(request.POST, instance=member.user)
            if account_form.is_valid():
                account_form.save()
                messages.success(request, "Compte mis a jour.")
                return redirect("user_account_edit", member_id=member.id)
        elif form_name == "password":
            password_form = SetPasswordForm(user=member.user, data=request.POST)
            _apply_bootstrap_classes(password_form)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Mot de passe reinitialise.")
                return redirect("user_account_edit", member_id=member.id)
        else:
            messages.error(request, "Action inconnue.")

    return render(
        request,
        "user_account_edit.html",
        {
            "member": member,
            "account_form": account_form,
            "password_form": password_form,
        },
    )


@staff_member_required(login_url="/login/")
@require_POST
def reject_application(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)

    if application.status != RecruitmentApplication.STATUS_PENDING:
        messages.warning(request, "Cette candidature a deja ete traitee.")
        return redirect("admin_panel")

    application.status = RecruitmentApplication.STATUS_REJECTED
    application.admin_note = request.POST.get("admin_note", "").strip()
    application.reviewed_at = timezone.now()
    application.reviewed_by = request.user
    application.save(update_fields=["status", "admin_note", "reviewed_at", "reviewed_by"])

    messages.success(request, "Candidature refusee.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def accept_match_request(request, pk):
    match_request = get_object_or_404(MatchRequest, pk=pk)

    if match_request.status != MatchRequest.STATUS_PENDING:
        messages.warning(request, "Cette demande a deja ete traitee.")
        return redirect("admin_panel")

    match_request.status = MatchRequest.STATUS_ACCEPTED
    match_request.admin_note = request.POST.get("admin_note", "").strip()
    match_request.reviewed_at = timezone.now()
    match_request.reviewed_by = request.user
    match_request.save(update_fields=["status", "admin_note", "reviewed_at", "reviewed_by"])

    messages.success(request, "Demande de match acceptee.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def reject_match_request(request, pk):
    match_request = get_object_or_404(MatchRequest, pk=pk)

    if match_request.status != MatchRequest.STATUS_PENDING:
        messages.warning(request, "Cette demande a deja ete traitee.")
        return redirect("admin_panel")

    match_request.status = MatchRequest.STATUS_REJECTED
    match_request.admin_note = request.POST.get("admin_note", "").strip()
    match_request.reviewed_at = timezone.now()
    match_request.reviewed_by = request.user
    match_request.save(update_fields=["status", "admin_note", "reviewed_at", "reviewed_by"])

    messages.success(request, "Demande de match refusee.")
    return redirect("admin_panel")


@staff_member_required(login_url="/login/")
@require_POST
def delete_match_request(request, pk):
    if request.user.username != "admin":
        messages.error(
            request,
            "Seul l'utilisateur admin peut supprimer une demande de match.",
        )
        return redirect("admin_panel")

    match_request = get_object_or_404(MatchRequest, pk=pk)
    match_request.delete()
    messages.success(request, "Demande de match supprimee de l'historique.")
    return redirect("admin_panel")
