# Generated by Django 3.2.12 on 2024-07-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0018_rename_nom_chapitre_chapitre_nom'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='ID_chap',
            field=models.IntegerField(default=0),
        ),
    ]