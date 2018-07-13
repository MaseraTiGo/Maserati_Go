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

from model.models import Customer

from tuoen.abs.service.customer.salechance import SaleChanceHelper

class CustomerServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询客户列表"""

        customer_qs = cls.search_qs(**search_info)

        return Splitor(current_page, customer_qs)

    @classmethod
    def get(cls, customer_id):
        """查询客户详情"""

        customer = Customer.get_byid(customer_id)
        if customer is None:
            raise BusinessError("客户不存在")
        return customer

    @classmethod
    def update(cls, customer, **attr):
        """修改客户信息"""

        customer.update(**attr)
        return customer

    @classmethod
    def search_qs(cls, **search_info):
        """查询客户列表"""

        customer_qs = Customer.search(**search_info)
        customer_qs.order_by("-create_time")
        return customer_qs

class SaleChanceServer(object):

    @classmethod
    def generate(cls, **attr):
        """生成销售机会列表"""

        return SaleChanceHelper.generate(**attr)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询销售机会列表"""

        return SaleChanceHelper.search(current_page, **search_info)

    @classmethod
    def update(cls, sale_chance_id, **attrs):
        """更新销售机会列表"""

        return SaleChanceHelper.update(sale_chance_id, **attrs)

    @classmethod
    def get(cls, sale_chance_id):
        """获取销售机会详情"""

        return SaleChanceHelper.get(sale_chance_id)
