# Generated by Django 3.2.12 on 2024-06-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='num_mail',
            field=models.IntegerField(default=0),
        ),
    ]
