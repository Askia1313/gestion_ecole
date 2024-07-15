# Generated by Django 3.2.12 on 2024-07-08 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0019_cours_id_chap'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='cours',
            field=models.FileField(default='', upload_to='media/'),
        ),
        migrations.AddField(
            model_name='cours',
            name='cours_types',
            field=models.CharField(blank=True, choices=[('.pdf', 'texte'), ('.mp3', 'video')], max_length=4, null=True),
        ),
    ]
