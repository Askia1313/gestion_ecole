# Generated by Django 3.2.12 on 2024-05-31 08:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_alter_customuser_type_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type_transaction',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
    ]
