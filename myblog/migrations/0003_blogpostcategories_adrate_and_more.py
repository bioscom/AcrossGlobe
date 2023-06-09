# Generated by Django 4.2.1 on 2023-05-15 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_blogpostcategories_moderatoremail'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostcategories',
            name='adrate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='adrate'),
        ),
        migrations.AddField(
            model_name='blogpostcategories',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='discount'),
        ),
        migrations.AddField(
            model_name='blogpostcategories',
            name='sub_title',
            field=models.CharField(blank=True, max_length=355, verbose_name='sub_title'),
        ),
    ]
