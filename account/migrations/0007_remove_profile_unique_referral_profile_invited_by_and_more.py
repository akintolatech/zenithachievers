# Generated by Django 5.1.6 on 2025-02-09 10:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_unique_referral'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='unique_referral',
        ),
        migrations.AddField(
            model_name='profile',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='referral_link',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
