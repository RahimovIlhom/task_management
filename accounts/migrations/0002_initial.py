# Generated by Django 5.0.7 on 2024-07-18 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classname',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_app.course'),
        ),
        migrations.AddField(
            model_name='profile',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.classname'),
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_app.course'),
        ),
    ]
