# Generated by Django 4.1.6 on 2023-02-13 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0011_alter_client_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.IntegerField(),
        ),
    ]
