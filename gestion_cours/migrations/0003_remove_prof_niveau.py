# Generated by Django 3.2.12 on 2024-07-03 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0002_auto_20240703_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prof',
            name='niveau',
        ),
    ]
