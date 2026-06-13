from django.db import models


class TeamSettings(models.Model):
    team_name = models.CharField(max_length=100, default="WarToWin")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    welcome_text = models.TextField()

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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pseudo} - {self.get_status_display()}"


class Rule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
