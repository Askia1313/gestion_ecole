# Generated by Django 3.2.12 on 2024-06-19 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0008_customuser_num_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='choix',
            field=models.IntegerField(default=0),
        ),
    ]