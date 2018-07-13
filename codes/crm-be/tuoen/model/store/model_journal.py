# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff


class JournalTypes(object):
    LOGIN = "login"
    OTHER = "other"
    CHOICES = ((LOGIN, '登录'), (OTHER, "其它"))


class OperationTypes(object):
    STAFF = "staff"
    USER = "user"
    SYSTEM = "system"
    CHOICES = ((STAFF, '员工'), (USER, "用户"), (SYSTEM, "系统"))


class Journal(BaseModel):
    """日志表"""
    active_uid = IntegerField(verbose_name = "主动方uid", default = 0)
    active_name = CharField(verbose_name = "主动方姓名", max_length = 128)
    active_type = CharField(verbose_name = "主动方类型", max_length = 64, choices = OperationTypes.CHOICES, default = OperationTypes.SYSTEM)
    passive_uid = IntegerField(verbose_name = "被动方uid", default = 0)
    passive_name = CharField(verbose_name = "被动方姓名", max_length = 128)
    passive_type = CharField(verbose_name = "被动方类型", max_length = 64, choices = OperationTypes.CHOICES, default = OperationTypes.SYSTEM)
    journal_type = CharField(verbose_name = "日志类型", max_length = 64, choices = JournalTypes.CHOICES, default = JournalTypes.OTHER)
    record_detail = TextField(verbose_name = "详情")
    remark = TextField(verbose_name="备注")

    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        journal_qs = cls.query().filter(**attrs)
        return journal_qs

