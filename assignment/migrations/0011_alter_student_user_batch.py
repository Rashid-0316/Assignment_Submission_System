# Generated by Django 3.2.7 on 2021-10-04 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_batch_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_user',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='assignment.batch'),
        ),
    ]
