# Generated by Django 4.1.6 on 2023-02-10 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelTable(
            name='client',
            table='clients',
        ),
    ]
