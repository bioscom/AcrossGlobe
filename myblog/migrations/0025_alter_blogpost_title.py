# Generated by Django 4.2.1 on 2023-06-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0024_alter_blogpost_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
    ]
