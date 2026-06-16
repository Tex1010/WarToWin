from django import forms
from .models import (
    Interim,
    Leader,
    MatchRequest,
    Member,
    RecruitmentApplication,
    Rule,
    TeamSettings,
)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "pseudo", "photo", "ff_profile_photo", "slogan"]
        labels = {
            "name": "Nom complet",
            "pseudo": "Pseudo",
            "photo": "Photo du membre",
            "ff_profile_photo": "Photo de profil Free Fire",
            "slogan": "Slogan",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "pseudo": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "ff_profile_photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "slogan": forms.TextInput(attrs={"class": "form-control"}),
        }


class LeaderForm(forms.ModelForm):
    class Meta:
        model = Leader
        fields = ["name", "pseudo", "photo", "ff_profile_photo", "slogan"]
        labels = {
            "name": "Nom complet",
            "pseudo": "Pseudo",
            "photo": "Photo du leader",
            "ff_profile_photo": "Photo de profil Free Fire",
            "slogan": "Slogan",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "pseudo": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "ff_profile_photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "slogan": forms.TextInput(attrs={"class": "form-control"}),
        }


class InterimForm(forms.ModelForm):
    class Meta:
        model = Interim
        fields = ["name", "pseudo", "photo", "ff_profile_photo", "slogan"]
        labels = {
            "name": "Nom complet",
            "pseudo": "Pseudo",
            "photo": "Photo de l'interim",
            "ff_profile_photo": "Photo de profil Free Fire",
            "slogan": "Slogan",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "pseudo": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "ff_profile_photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".png,.jpg,.jpeg,.webp"}
            ),
            "slogan": forms.TextInput(attrs={"class": "form-control"}),
        }


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ["title", "description"]


class TeamSettingsForm(forms.ModelForm):
    class Meta:
        model = TeamSettings
        fields = [
            "team_tag",
            "team_name",
            "welcome_text",
            "logo",
            "font_choice",
            "background_color",
            "background_soft_color",
            "card_color",
            "card_soft_color",
            "primary_color",
            "primary_soft_color",
            "accent_color",
            "text_color",
            "muted_color",
        ]
        labels = {
            "team_tag": "Tag de la team",
            "team_name": "Nom de la team",
            "welcome_text": "Texte d'accueil",
            "logo": "Logo de la team",
            "font_choice": "Police du site",
            "background_color": "Couleur de fond",
            "background_soft_color": "Fond secondaire",
            "card_color": "Couleur des cartes",
            "card_soft_color": "Couleur des cartes secondaires",
            "primary_color": "Couleur principale",
            "primary_soft_color": "Couleur principale secondaire",
            "accent_color": "Couleur d'accent",
            "text_color": "Couleur du texte",
            "muted_color": "Couleur du texte secondaire",
        }
        widgets = {
            "team_tag": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: W2W",
                    "maxlength": 20,
                }
            ),
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
            "font_choice": forms.Select(attrs={"class": "form-select"}),
            "background_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "background_soft_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "card_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "card_soft_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "primary_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "primary_soft_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "accent_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "text_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
            "muted_color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
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
            "facebook_profile",
            "motivation",
            "profile_photo",
            "profile_screenshot",
        ]
        labels = {
            "full_name": "Nom complet",
            "pseudo": "Pseudo Free Fire",
            "free_fire_uid": "UID Free Fire",
            "level": "Niveau de jeu",
            "whatsapp": "Numero WhatsApp",
            "facebook_profile": "Nom ou lien du profil Facebook",
            "motivation": "Pourquoi veux-tu rejoindre la team ?",
            "profile_photo": "Photo de profil",
            "profile_screenshot": "Capture du profil Free Fire",
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: TENDRY Tahinjanahary",
                    "autocomplete": "name",
                }
            ),
            "pseudo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Shadow",
                    "autocapitalize": "off",
                    "spellcheck": "false",
                }
            ),
            "free_fire_uid": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 6017178292",
                    "inputmode": "numeric",
                }
            ),
            "level": forms.Select(attrs={"class": "form-select"}),
            "whatsapp": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: +261 34 77 947 91",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "facebook_profile": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Tendry Tahinjanahary ou https://facebook.com/...",
                    "autocomplete": "url",
                }
            ),
            "motivation": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Parle de ton niveau, ta disponibilite, ton objectif en team et pourquoi WarToWin.",
                }
            ),
            "profile_photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".png,.jpg,.jpeg,.webp",
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

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")

        if not photo:
            raise forms.ValidationError("La photo de profil est obligatoire.")

        allowed_content_types = {
            "image/png",
            "image/jpeg",
            "image/webp",
        }

        if photo.content_type not in allowed_content_types:
            raise forms.ValidationError(
                "Formats acceptes: PNG, JPG, JPEG ou WEBP."
            )

        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Le fichier depasse 5 Mo. Choisis une image plus legere."
            )

        return photo


class MatchRequestForm(forms.ModelForm):
    requested_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = MatchRequest
        fields = [
            "requester_name",
            "contact_info",
            "request_type",
            "requested_at",
            "message",
        ]
        labels = {
            "requester_name": "Nom du visiteur ou de la team",
            "contact_info": "Contact (WhatsApp, Facebook ou autre)",
            "request_type": "Type de demande",
            "requested_at": "Date et heure souhaitees",
            "message": "Message",
        }
        widgets = {
            "requester_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: W2W Team",
                }
            ),
            "contact_info": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: +261 34 77 947 91 ou lien Facebook",
                }
            ),
            "request_type": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Ajoute un detail utile pour la demande.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["request_type"].choices = [
            ("", "Choisis TvT ou TvG"),
            *MatchRequest.REQUEST_TYPE_CHOICES,
        ]
