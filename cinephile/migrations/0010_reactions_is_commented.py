# Generated by Django 5.1.4 on 2025-01-10 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinephile', '0009_aspirantposts_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='reactions',
            name='is_commented',
            field=models.BooleanField(default=False),
        ),
    ]
