# Generated by Django 4.2.1 on 2023-07-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='eventtype',
            field=models.CharField(blank=True, choices=[('In Person', 'In Person'), ('Virtual', 'Virtual')], max_length=15, null=True),
        ),
    ]
