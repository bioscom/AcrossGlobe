# Generated by Django 4.2.1 on 2023-09-03 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0039_blogpostcategories_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostcategories',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('Discount', 'Discount'), ('Premium', 'Premium')], max_length=20, null=True),
        ),
    ]
