# Generated by Django 3.2.12 on 2024-05-31 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0005_rename_tel_customuser_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
