# Generated by Django 4.2.1 on 2023-08-05 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_events_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]