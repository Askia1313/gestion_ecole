# Generated by Django 3.2.12 on 2024-07-07 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0008_cours_nom_matiere'),
    ]

    operations = [
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_niveau', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='cours',
            name='cours_lien',
        ),
        migrations.RemoveField(
            model_name='cours',
            name='email_prof',
        ),
        migrations.RemoveField(
            model_name='cours',
            name='nom_matiere',
        ),
        migrations.RemoveField(
            model_name='cours',
            name='type_cours',
        ),
        migrations.AddField(
            model_name='cours',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='matiere',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gestion_cours.matiere'),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='nom_chapitre',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='cours',
            name='chapitre',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gestion_cours.chapitre'),
        ),
        migrations.AlterField(
            model_name='cours',
            name='nom_cours',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='matiere',
            name='nom_matiere',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='Exercice',
        ),
        migrations.AddField(
            model_name='matiere',
            name='niveau',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='gestion_cours.niveau'),
        ),
    ]