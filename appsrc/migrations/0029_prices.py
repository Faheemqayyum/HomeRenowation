# Generated by Django 5.0 on 2024-05-03 05:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appsrc", "0028_feedback"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prices",
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
                ("category", models.CharField(max_length=1000)),
                ("hour_price", models.IntegerField(default=500)),
                ("daily_price", models.IntegerField(default=1200)),
            ],
        ),
    ]