# Generated by Django 4.1.4 on 2024-01-16 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_profile_location_skill"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="social_gihub", new_name="social_github",
        ),
    ]
