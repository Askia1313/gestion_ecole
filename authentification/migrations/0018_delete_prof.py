# Generated by Django 3.2.12 on 2024-07-04 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0017_auto_20240704_1314'),
        ('gestion_cours', '0005_auto_20240704_1314'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Prof',
        ),
    ]