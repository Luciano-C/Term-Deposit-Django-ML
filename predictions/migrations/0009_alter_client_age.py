# Generated by Django 4.1.6 on 2023-02-13 15:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0008_alter_client_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=18, message='Number must be higher than 18'), django.core.validators.MaxValueValidator(120)]),
        ),
    ]
