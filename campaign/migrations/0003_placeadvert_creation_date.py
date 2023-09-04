# Generated by Django 4.2.1 on 2023-08-30 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_advertisement_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeadvert',
            name='creation_date',
            field=models.DateField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]