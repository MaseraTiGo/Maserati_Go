# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_customer import Customer
from model.store.model_order import Order, OrderItem


class Logistics(BaseModel):
    order = ForeignKey(Order)
    customer = ForeignKey(Customer)

    company = CharField(verbose_name = "物流公司", max_length = 64, default = "", null = True)
    number = CharField(verbose_name = "物流单号", max_length = 64, default = "", null = True)
    total_quantity = IntegerField(verbose_name = "发货数量")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


class LogisticsItem(BaseModel):
    customer = ForeignKey(Customer)
    logistics = ForeignKey(Logistics)

    order_item = ForeignKey(OrderItem)
    quantity = IntegerField(verbose_name = "数量")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
