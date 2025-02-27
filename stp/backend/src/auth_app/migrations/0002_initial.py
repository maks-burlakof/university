# Generated by Django 5.1.1 on 2024-10-12 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth_app", "0001_initial"),
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersessions",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users_app.user"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="usersessions",
            unique_together={("ipv4", "user_agent", "user")},
        ),
    ]
