# Generated by Django 5.0.7 on 2024-07-25 23:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_historicaluser_deleted_at_user_deleted_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaluser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_active",
        ),
    ]
