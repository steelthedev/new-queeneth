# Generated by Django 4.2.4 on 2023-10-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_student_department_alter_student_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
