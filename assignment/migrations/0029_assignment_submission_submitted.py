# Generated by Django 3.2.7 on 2021-10-23 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0028_alter_assignment_submission_submission_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment_submission',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
