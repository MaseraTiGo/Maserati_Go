# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_order import Order

class StaffOrderEvent(BaseModel):
    """员工下单事件表"""
    staff = ForeignKey(Staff)
    order = ForeignKey(Order)

    describe = TextField(verbose_name = "描述", null = True, default = "")

    remark = TextField(verbose_name = "备注", null = True, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        event_qs = cls.query().filter(**attrs)
        return event_qs
