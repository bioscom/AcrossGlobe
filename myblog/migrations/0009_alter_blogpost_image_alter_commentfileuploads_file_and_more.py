# Generated by Django 4.2.1 on 2023-05-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_alter_comment_options_comment_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='FileUploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='commentfileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='FileUploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='fileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='FileUploads/%Y/%m/%d/'),
        ),
    ]
