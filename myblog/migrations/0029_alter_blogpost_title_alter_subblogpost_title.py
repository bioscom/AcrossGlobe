# Generated by Django 4.2.1 on 2023-06-12 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0028_alter_blogpost_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='subblogpost',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
    ]
