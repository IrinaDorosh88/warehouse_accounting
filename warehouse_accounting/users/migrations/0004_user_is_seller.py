# Generated by Django 4.2.5 on 2023-10-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_seller",
            field=models.BooleanField(default=False),
        ),
    ]
