# Generated by Django 4.1.6 on 2023-02-16 15:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0013_client_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='date',
        ),
        migrations.AddField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
