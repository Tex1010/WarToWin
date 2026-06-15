from django.db import models
from django.conf import settings


class TeamSettings(models.Model):
    FONT_TECH = "orbitron"
    FONT_MODERN = "poppins"
    FONT_GAMING = "rajdhani"

    FONT_CHOICES = [
        (FONT_TECH, "Orbitron + Inter"),
        (FONT_MODERN, "Poppins"),
        (FONT_GAMING, "Rajdhani"),
    ]

    team_tag = models.CharField(max_length=20, default="W2W")
    team_name = models.CharField(max_length=100, default="WarToWin")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    welcome_text = models.TextField()
    font_choice = models.CharField(
        max_length=20,
        choices=FONT_CHOICES,
        default=FONT_TECH,
    )
    background_color = models.CharField(max_length=7, default="#050507")
    background_soft_color = models.CharField(max_length=7, default="#0f0a0d")
    card_color = models.CharField(max_length=7, default="#121116")
    card_soft_color = models.CharField(max_length=7, default="#17141c")
    primary_color = models.CharField(max_length=7, default="#ff274b")
    primary_soft_color = models.CharField(max_length=7, default="#ff5c78")
    accent_color = models.CharField(max_length=7, default="#00b16a")
    text_color = models.CharField(max_length=7, default="#ffffff")
    muted_color = models.CharField(max_length=7, default="#a7acba")

    def __str__(self):
        return self.team_name


class Leader(models.Model):
    name = models.CharField(max_length=100)
    pseudo = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="leaders/",
        blank=True,
        null=True
    )
    ff_profile_photo = models.ImageField(
        upload_to="leaders/ff_profiles/",
        blank=True,
        null=True
    )

    slogan = models.CharField(
        max_length=255,
        blank=True
    )

    role = models.CharField(
        max_length=100,
        default="Leader"
    )

    def __str__(self):
        return self.pseudo

class Interim(models.Model):
    name = models.CharField(max_length=100)
    pseudo = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="interims/",
        blank=True,
        null=True
    )
    ff_profile_photo = models.ImageField(
        upload_to="interims/ff_profiles/",
        blank=True,
        null=True
    )

    slogan = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.pseudo


class Member(models.Model):
    name = models.CharField(max_length=100)
    pseudo = models.CharField(max_length=100, unique=True)

    photo = models.ImageField(
        upload_to="members/",
        blank=True,
        null=True
    )
    ff_profile_photo = models.ImageField(
        upload_to="members/ff_profiles/",
        blank=True,
        null=True
    )

    slogan = models.CharField(
        max_length=255,
        blank=True
    )

    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pseudo} ({self.name})"


class RecruitmentApplication(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_ACCEPTED, "Acceptee"),
        (STATUS_REJECTED, "Refusee"),
    ]

    LEVEL_BEGINNER = "debutant"
    LEVEL_INTERMEDIATE = "intermediaire"
    LEVEL_ADVANCED = "avance"
    LEVEL_COMPETITIVE = "competitif"

    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, "Debutant"),
        (LEVEL_INTERMEDIATE, "Intermediaire"),
        (LEVEL_ADVANCED, "Avance"),
        (LEVEL_COMPETITIVE, "Competitif"),
    ]

    full_name = models.CharField(max_length=100)
    pseudo = models.CharField(max_length=100)
    free_fire_uid = models.CharField(max_length=20)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    whatsapp = models.CharField(max_length=30, blank=True)
    facebook_profile = models.CharField(max_length=255, blank=True)
    motivation = models.TextField()
    profile_screenshot = models.ImageField(upload_to="applications/")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviewed_recruitment_applications",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pseudo} - {self.get_status_display()}"


class MatchRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_ACCEPTED, "Acceptee"),
        (STATUS_REJECTED, "Refusee"),
    ]

    TYPE_TVT = "tvt"
    TYPE_TVG = "tvg"

    REQUEST_TYPE_CHOICES = [
        (TYPE_TVT, "TvT"),
        (TYPE_TVG, "TvG"),
    ]

    requester_name = models.CharField(max_length=120)
    contact_info = models.CharField(max_length=255, blank=True)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    requested_at = models.DateTimeField()
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviewed_match_requests",
    )

    class Meta:
        ordering = ["requested_at", "-created_at"]

    def __str__(self):
        return f"{self.requester_name} - {self.get_request_type_display()}"


class Rule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
