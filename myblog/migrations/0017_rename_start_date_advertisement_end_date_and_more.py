# Generated by Django 4.2.1 on 2023-06-07 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0016_alter_blogpost_thumbnails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='start_date',
            new_name='end_date',
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myblog.blogpostcategories'),
        ),
    ]
