# Generated by Django 3.2.7 on 2021-09-20 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_alter_department_hod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hod_user',
            name='hod',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hod', to=settings.AUTH_USER_MODEL),
        ),
    ]
