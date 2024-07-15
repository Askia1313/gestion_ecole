# Generated by Django 3.2.12 on 2024-07-07 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0014_auto_20240707_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapitre',
            name='matiere',
            field=models.CharField(blank=True, choices=[('MATHEMATIQUE', '6eme'), ('PHYSIQUE-CHIMIE', '5eme'), ('HISTOIRE-GEOGRAPHIE', '4eme'), ('ANGLAIS', '3eme'), ('PHILOSOPHIE', '2nd'), ('ALLEMAND', '1ere'), ('SVT', 'Tle')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='niveau',
            field=models.CharField(blank=True, choices=[('6e', '6eme'), ('5e', '5eme'), ('4e', '4eme'), ('3e', '3eme'), ('2nd', '2nd'), ('1ere', '1ere'), ('Tle', 'Tle')], max_length=4, null=True),
        ),
        migrations.DeleteModel(
            name='Matiere',
        ),
    ]