# Generated by Django 5.1.6 on 2025-02-08 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deposit',
            options={'ordering': ['-created']},
        ),
    ]
