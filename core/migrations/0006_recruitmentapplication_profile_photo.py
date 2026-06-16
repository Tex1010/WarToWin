from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_matchrequest_reviewed_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruitmentapplication",
            name="profile_photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="applications/profile_photos/",
            ),
        ),
    ]
