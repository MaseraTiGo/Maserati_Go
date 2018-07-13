# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_customer import Customer
from model.store.model_mobilephone import Mobilephone


class TrackEvent(BaseModel):
    """跟踪事件表"""
    customer = ForeignKey(Customer)
    staff = ForeignKey(Staff, null = True)
    describe = TextField(verbose_name = "描述")

    remark = TextField(verbose_name = "备注")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        track_event_qs = cls.query().filter(**attrs)
        return track_event_qs
