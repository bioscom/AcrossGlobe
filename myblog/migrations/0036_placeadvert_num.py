# Generated by Django 4.2.1 on 2023-08-30 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0035_remove_advertisement_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeadvert',
            name='num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
