# Generated by Django 5.1.6 on 2025-02-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_amount_withdrawn_profile_app_earnings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='total_sent_transfers',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_whatsapp_withdrawal',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='whatsapp_earnings',
            field=models.IntegerField(default=4),
        ),
    ]
