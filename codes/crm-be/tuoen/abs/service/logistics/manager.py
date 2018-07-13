# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.models import Logistics, LogisticsItem


class LogisticsServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询物流列表"""

        logistics_qs = Logistics.query(**search_info)

        return logistics_qs

    @classmethod
    def hung_item_fororser(cls, order):
        """订单挂载物流"""

        logistics_qs = cls.search(order = order)
        for logistics in logistics_qs:
            LogisticsItemServer.hung_item_forlogistics(logistics)

        order.logistics = logistics_qs

        return order

class LogisticsItemServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询物流详情列表"""

        logistics_item_qs = LogisticsItem.query(**search_info)

        return logistics_item_qs

    @classmethod
    def hung_item_forlogistics(cls, logistics):
        """物流详情挂在物流"""

        logistics.items = cls.search(logistics = logistics)

        return logistics
