from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecruitmentApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=100)),
                ("pseudo", models.CharField(max_length=100)),
                ("free_fire_uid", models.CharField(max_length=20)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("debutant", "Debutant"),
                            ("intermediaire", "Intermediaire"),
                            ("avance", "Avance"),
                            ("competitif", "Competitif"),
                        ],
                        max_length=20,
                    ),
                ),
                ("whatsapp", models.CharField(blank=True, max_length=30)),
                ("motivation", models.TextField()),
                ("profile_screenshot", models.ImageField(upload_to="applications/")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "En attente"),
                            ("accepted", "Acceptee"),
                            ("rejected", "Refusee"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("admin_note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
