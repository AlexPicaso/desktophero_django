# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20170603_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='mesh_hires',
            field=models.FileField(null=True, upload_to=b'meshes'),
        ),
        migrations.AddField(
            model_name='asset',
            name='mesh_lowres',
            field=models.FileField(null=True, upload_to=b'meshes'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='category',
            field=models.CharField(default=b'unknown', max_length=30),
        ),
        migrations.AlterField(
            model_name='asset',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
