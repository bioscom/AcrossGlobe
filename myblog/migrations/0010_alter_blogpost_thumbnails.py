# Generated by Django 4.2.1 on 2023-05-31 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0009_alter_blogpost_image_alter_commentfileuploads_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnails',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/%Y/%m/%d/'),
        ),
    ]