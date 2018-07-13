# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-29 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64, verbose_name='姓名')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('city', models.CharField(max_length=128, verbose_name='城市')),
                ('address', models.CharField(max_length=128, verbose_name='详细地址')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=64, verbose_name='账号')),
                ('passwd', models.CharField(max_length=64, verbose_name='密码')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号')),
                ('role_type', models.IntegerField(choices=[(0, '用户角色'), (1, '医生角色'), (10, '第三方检测机构员工'), (99, '员工角色')], verbose_name='角色类型')),
                ('nick', models.CharField(default='', max_length=64, verbose_name='昵称')),
                ('photo_url', models.CharField(default='', max_length=256, verbose_name='头像')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='最后一次登录时间')),
                ('last_version', models.CharField(default='2.0.1', max_length=32, verbose_name='最后一个版本信息')),
                ('last_platform', models.CharField(default='', max_length=32, verbose_name='最后一次的平台信息')),
                ('plat_type', models.IntegerField(choices=[(0, '未知'), (1, 'android'), (2, 'iphone'), (3, 'crm'), (3, 'organization')], default=0, verbose_name='注册平台')),
                ('source', models.CharField(choices=[('360', '360'), ('91', '91'), ('anzhi', '安智'), ('baidu', '百度'), ('flyme', '魅族'), ('oppo', 'oppo'), ('qq', 'qq'), ('uc', 'uc'), ('xiaomi', '小米'), ('web', '网站'), ('app_store', '苹果商店'), ('unknow', '未知')], default='unknow', max_length=32, verbose_name='来源')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='model.User'),
        ),
    ]