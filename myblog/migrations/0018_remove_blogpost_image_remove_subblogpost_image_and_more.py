# Generated by Django 4.2.1 on 2023-06-09 11:56

from django.db import migrations, models
import myblog.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0017_rename_start_date_advertisement_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='image',
        ),
        migrations.RemoveField(
            model_name='subblogpost',
            name='image',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image1',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image2',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image3',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image4',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='subblogpost',
            name='image1',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='subblogpost',
            name='image2',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='subblogpost',
            name='image3',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AddField(
            model_name='subblogpost',
            name='image4',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=myblog.models.renameadfiles),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnails',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamethumbnails, verbose_name='thumbnails'),
        ),
        migrations.AlterField(
            model_name='commentfileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AlterField(
            model_name='fileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AlterField(
            model_name='subblogpost',
            name='thumbnails',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamethumbnails),
        ),
        migrations.AlterField(
            model_name='subcommentfileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
        migrations.AlterField(
            model_name='subfileuploads',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=myblog.models.renamefile),
        ),
    ]