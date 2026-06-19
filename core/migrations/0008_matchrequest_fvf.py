from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_member_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matchrequest",
            name="request_type",
            field=models.CharField(
                choices=[("tvt", "TvT"), ("tvg", "TvG"), ("fvf", "FvF")],
                max_length=10,
            ),
        ),
    ]
