# Generated by Django 4.1.6 on 2023-02-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0005_client_balance_client_campaign_client_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='education',
            field=models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary'), ('tertiary', 'tertiary'), ('unknown', 'unknown')], max_length=100),
        ),
    ]
