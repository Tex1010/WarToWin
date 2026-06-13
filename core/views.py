from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    InterimForm,
    LeaderForm,
    MemberForm,
    RecruitmentForm,
    RuleForm,
    TeamSettingsForm,
)
from .models import (
    Interim,
    Leader,
    Member,
    RecruitmentApplication,
    Rule,
    TeamSettings,
)


def home(request):
    settings = get_team_settings()
    leaders = Leader.objects.all()
    interims = Interim.objects.all()
    members_count = Member.objects.count()

    return render(
        request,
        "index.html",
        {
            "settings": settings,
            "leaders": leaders,
            "interims": interims,
            "members_count": members_count,
        },
    )


def members(request):
    context = {
        "leaders": Leader.objects.all(),
        "interims": Interim.objects.all(),
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


def get_team_settings():
    settings = TeamSettings.objects.first()

    if settings:
        return settings

    settings = TeamSettings.objects.create(
        team_name="War To Win",
        welcome_text="Une team mobile ambitieuse, disciplinee et prete pour les prochains defis.",
    )
    return settings


def build_admin_context():
    team_settings = get_team_settings()
    pending_applications = RecruitmentApplication.objects.filter(
        status=RecruitmentApplication.STATUS_PENDING
    )
    reviewed_applications = RecruitmentApplication.objects.exclude(
        status=RecruitmentApplication.STATUS_PENDING
    )

    return {
        "members": Member.objects.all(),
        "leaders": Leader.objects.all(),
        "interims": Interim.objects.all(),
        "rules": Rule.objects.all(),
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
    }


@staff_member_required(login_url="/admin/login/")
def admin_panel(request):
    return render(request, "admin_panel.html", build_admin_context())


@staff_member_required(login_url="/admin/login/")
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


@staff_member_required(login_url="/admin/login/")
@require_POST
def add_member(request):
    form = MemberForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Membre ajoute avec succes.")
    else:
        messages.error(request, "Impossible d'ajouter le membre.")

    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
def add_leader(request):
    form = LeaderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Leader ajoute avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Ajouter un leader"})


@staff_member_required(login_url="/admin/login/")
def add_interim(request):
    form = InterimForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Interim ajoute avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Ajouter un interim"})


@staff_member_required(login_url="/admin/login/")
def add_rule(request):
    form = RuleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reglement ajoute avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Ajouter un reglement"})


@staff_member_required(login_url="/admin/login/")
def edit_rule(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    form = RuleForm(request.POST or None, instance=rule)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reglement modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un reglement"})


@staff_member_required(login_url="/admin/login/")
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, request.FILES or None, instance=member)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Membre modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un membre"})


@staff_member_required(login_url="/admin/login/")
def edit_leader(request, pk):
    leader = get_object_or_404(Leader, pk=pk)
    form = LeaderForm(request.POST or None, request.FILES or None, instance=leader)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Leader modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un leader"})


@staff_member_required(login_url="/admin/login/")
def edit_interim(request, pk):
    interim = get_object_or_404(Interim, pk=pk)
    form = InterimForm(request.POST or None, request.FILES or None, instance=interim)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Interim modifie avec succes.")
        return redirect("admin_panel")

    return render(request, "form.html", {"form": form, "title": "Modifier un interim"})


@staff_member_required(login_url="/admin/login/")
@require_POST
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    messages.success(request, "Membre supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
@require_POST
def delete_leader(request, pk):
    leader = get_object_or_404(Leader, pk=pk)
    leader.delete()
    messages.success(request, "Leader supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
@require_POST
def delete_interim(request, pk):
    interim = get_object_or_404(Interim, pk=pk)
    interim.delete()
    messages.success(request, "Interim supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
@require_POST
def delete_rule(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    messages.success(request, "Reglement supprime.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
@require_POST
def delete_application(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    application.delete()
    messages.success(request, "Candidature supprimee de l'historique.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
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
        Member.objects.create(
            name=application.full_name,
            pseudo=application.pseudo,
            slogan=f"Niveau {application.get_level_display()}",
        )
        application.status = RecruitmentApplication.STATUS_ACCEPTED
        application.admin_note = admin_note
        application.reviewed_at = timezone.now()
        application.save(update_fields=["status", "admin_note", "reviewed_at"])

    messages.success(request, "Candidature acceptee et membre ajoute.")
    return redirect("admin_panel")


@staff_member_required(login_url="/admin/login/")
@require_POST
def reject_application(request, pk):
    application = get_object_or_404(RecruitmentApplication, pk=pk)

    if application.status != RecruitmentApplication.STATUS_PENDING:
        messages.warning(request, "Cette candidature a deja ete traitee.")
        return redirect("admin_panel")

    application.status = RecruitmentApplication.STATUS_REJECTED
    application.admin_note = request.POST.get("admin_note", "").strip()
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "admin_note", "reviewed_at"])

    messages.success(request, "Candidature refusee.")
    return redirect("admin_panel")
