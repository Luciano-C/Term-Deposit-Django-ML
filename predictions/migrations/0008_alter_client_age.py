# Generated by Django 4.1.6 on 2023-02-13 15:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0007_alter_client_balance_alter_client_campaign_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(120)]),
        ),
    ]
