# Generated by Django 4.1.4 on 2024-02-06 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_alter_project_options_review_owner_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["-vote_ratio", "-vote_total", "title"]},
        ),
        migrations.AlterField(
            model_name="review",
            name="value",
            field=models.CharField(
                choices=[("up", "Up Vote"), ("down", "Down Vote")], max_length=200
            ),
        ),
    ]
