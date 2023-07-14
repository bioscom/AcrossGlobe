# Generated by Django 4.2.1 on 2023-05-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_remove_advertisement_advertiser_advertisement_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='expiration_date',
            new_name='start_date',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]