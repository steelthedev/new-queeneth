# Generated by Django 4.2.4 on 2023-10-28 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_staff_image_staff_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
