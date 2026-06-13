from django import forms
from .models import (
    Interim,
    Leader,
    Member,
    RecruitmentApplication,
    Rule,
    TeamSettings,
)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "pseudo", "photo", "slogan"]


class LeaderForm(forms.ModelForm):
    class Meta:
        model = Leader
        fields = ["name", "pseudo", "photo", "slogan"]


class InterimForm(forms.ModelForm):
    class Meta:
        model = Interim
        fields = ["name", "pseudo", "photo", "slogan"]


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ["title", "description"]


class TeamSettingsForm(forms.ModelForm):
    class Meta:
        model = TeamSettings
        fields = ["team_name", "welcome_text", "logo"]
        labels = {
            "team_name": "Nom de la team",
            "welcome_text": "Texte d'accueil",
            "logo": "Logo de la team",
        }
        widgets = {
            "team_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: War To Win",
                }
            ),
            "welcome_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Ex: La team War To Win rassemble des joueurs motives, competitifs et solidaires.",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".png,.jpg,.jpeg,.webp",
                }
            ),
        }


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = RecruitmentApplication
        fields = [
            "full_name",
            "pseudo",
            "free_fire_uid",
            "level",
            "whatsapp",
            "motivation",
            "profile_screenshot",
        ]
        labels = {
            "full_name": "Nom complet",
            "pseudo": "Pseudo Free Fire",
            "free_fire_uid": "UID Free Fire",
            "level": "Niveau de jeu",
            "whatsapp": "Numero WhatsApp",
            "motivation": "Pourquoi veux-tu rejoindre la team ?",
            "profile_screenshot": "Capture du profil Free Fire",
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Jean Mavoungou",
                    "autocomplete": "name",
                }
            ),
            "pseudo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: WTW Shadow",
                    "autocapitalize": "off",
                    "spellcheck": "false",
                }
            ),
            "free_fire_uid": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 1234567890",
                    "inputmode": "numeric",
                }
            ),
            "level": forms.Select(attrs={"class": "form-select"}),
            "whatsapp": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: +242 06 123 45 67",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "motivation": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Parle de ton niveau, ta disponibilite, ton objectif en team et pourquoi WarToWin.",
                }
            ),
            "profile_screenshot": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".png,.jpg,.jpeg,.webp",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["level"].choices = [
            ("", "Choisis ton niveau"),
            *RecruitmentApplication.LEVEL_CHOICES,
        ]

    def clean_pseudo(self):
        pseudo = self.cleaned_data["pseudo"].strip()
        pending_application_exists = RecruitmentApplication.objects.filter(
            pseudo__iexact=pseudo,
            status=RecruitmentApplication.STATUS_PENDING,
        )

        if self.instance.pk:
            pending_application_exists = pending_application_exists.exclude(
                pk=self.instance.pk
            )

        if Member.objects.filter(pseudo__iexact=pseudo).exists():
            raise forms.ValidationError(
                "Ce pseudo appartient deja a un membre de la team."
            )

        if pending_application_exists.exists():
            raise forms.ValidationError(
                "Une candidature est deja en attente pour ce pseudo."
            )

        return pseudo

    def clean_free_fire_uid(self):
        uid = "".join(filter(str.isdigit, self.cleaned_data["free_fire_uid"]))

        if len(uid) < 6 or len(uid) > 20:
            raise forms.ValidationError("Entre un UID valide de 6 a 20 chiffres.")

        return uid

    def clean_profile_screenshot(self):
        screenshot = self.cleaned_data.get("profile_screenshot")

        if not screenshot:
            raise forms.ValidationError("La capture du profil est obligatoire.")

        allowed_content_types = {
            "image/png",
            "image/jpeg",
            "image/webp",
        }

        if screenshot.content_type not in allowed_content_types:
            raise forms.ValidationError(
                "Formats acceptes: PNG, JPG, JPEG ou WEBP."
            )

        if screenshot.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Le fichier depasse 5 Mo. Choisis une image plus legere."
            )

        return screenshot
