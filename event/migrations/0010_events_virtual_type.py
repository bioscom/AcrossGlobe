# Generated by Django 4.2.1 on 2023-08-08 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_alter_events_enddate_alter_events_endtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='virtual_type',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
