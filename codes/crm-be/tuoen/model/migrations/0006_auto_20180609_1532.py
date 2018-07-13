# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-09 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_auto_20180609_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='importcustomerbuyinfo',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importcustomerrebate',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importcustomerregister',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importcustomertransaction',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importequipmentin',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importequipmentout',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importmobiledevices',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importmobilephone',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
        migrations.AddField(
            model_name='importstaff',
            name='error_text',
            field=models.TextField(null=True, verbose_name='转化失败描述'),
        ),
    ]