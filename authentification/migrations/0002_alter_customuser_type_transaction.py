# Generated by Django 3.2.12 on 2024-05-31 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type_transaction',
            field=models.IntegerField(default=1),
        ),
    ]