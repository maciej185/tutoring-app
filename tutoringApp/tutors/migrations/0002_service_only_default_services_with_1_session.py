# Generated by Django 4.2.7 on 2023-12-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tutors", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="service",
            constraint=models.UniqueConstraint(
                condition=models.Q(("number_of_hours", 1)),
                fields=("subject", "tutor"),
                name="only_default_services_with_1_session",
                violation_error_message="One service with one sessions",
            ),
        ),
    ]
