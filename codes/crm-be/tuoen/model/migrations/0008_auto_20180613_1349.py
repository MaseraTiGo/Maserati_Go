# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-13 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0007_auto_20180611_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unpaid', '未支付'), ('submit', '已下单'), ('payed', '已支付'), ('sended', '已发货'), ('finished', '已发货')], default='submit', max_length=64, verbose_name='支付状态'),
        ),
    ]
