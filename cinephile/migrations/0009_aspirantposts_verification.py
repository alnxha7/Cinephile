# Generated by Django 5.1.4 on 2025-01-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinephile', '0008_alter_reactions_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspirantposts',
            name='verification',
            field=models.BooleanField(default=False),
        ),
    ]
