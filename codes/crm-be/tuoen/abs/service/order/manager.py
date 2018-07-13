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

from model.models import StaffOrderEvent, Order, OrderItem


class StaffOrderEventServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询事件列表"""

        staff_orser_event_qs = StaffOrderEvent.query(**search_info)

        staff_orser_event_qs = staff_orser_event_qs.order_by("-create_time")
        return Splitor(current_page, staff_orser_event_qs)


    @classmethod
    def get_event_byorder(cls, order):
        """通过订单查询事件"""

        try:
            return StaffOrderEvent.query(order = order)[0]
        except:
            return None

    @classmethod
    def get_event_bystaff(cls, staff_list):
        """通过员工查询事件"""

        try:
            return StaffOrderEvent.search(staff__in = staff_list)
        except:
            return []


class OrderServer(object):

    @classmethod
    def get(cls, order_id):
        """获取渠道详情"""

        order = Order.get_byid(order_id)
        if order is None:
            raise BusinessError("订单不存在")
        return order

    @classmethod
    def search_qs(cls, **search_info):
        user_pro = search_info.pop('cur_user')
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"pay_time__gte":begin_time})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"pay_time__lte":end_time})
        order_qs = Order.search(**search_info)
        if user_pro._is_admin:
            order_qs = Order.query()
        return order_qs

    @classmethod
    def search(cls, current_page, **search_info):
        """查询所有订单列表"""
        user_pro = search_info['cur_user']
        order_qs = cls.search_qs(**search_info)        
        if not user_pro._is_show_sub:
            event_id = StaffOrderEvent.query(staff_id__exact = user_pro._cur_user_id)[0].id
            order_qs = order_qs.filter(id__exact = event_id)
        order_qs = order_qs.order_by("-create_time")    
        return Splitor(current_page, order_qs)

    @classmethod
    def search_by_paytime(cls, search_time = None):
        """根据月份查询订单"""

        if search_time is None:
            current_time = datetime.datetime.now()
        else:
            current_time = search_time

        cur_date_first = datetime.datetime(current_time.year, current_time.month, 1)
        cur_date_last = datetime.datetime(current_time.year, current_time.month + 1, 1, 23, 59, 59) - datetime.timedelta(1)

        order_qs = cls.search_qs(begin_time = cur_date_first, end_time = cur_date_last, id__in = order_ids)

        return order_qs

    @classmethod
    def get_order_byevent(cls, event_list):
        """根据事件列表查询订单列表"""
        order_list = []
        for event in event_list:
            OrderItemServer.hung_item_fororder(event.order)
            order_list.append(event.order)

        return order_list

    @classmethod
    def get_order_byservice(cls, service_list):
        """根据服务单列表查询订单列表"""
        order_list = []
        for service in service_list:
            order_list.append(service.order)

        return order_list

    @classmethod
    def hung_shop_forservice(cls, service_item_list):
        """根据服务单详情挂载店铺"""
        order_ids = []
        for service_item in service_item_list:
            if service_item.service and service_item.service.order_id:
                order_ids.append(service_item.service.order_id)

        order_mapping = {}
        if len(order_ids) > 0:
            order_mapping = {order.id:order for order in \
                            Order.search(id__in = order_ids)}

        for service_item in service_item_list:
            service_item.shop = None
            if service_item.service and service_item.service.order_id:
                order = order_mapping.get(service_item.service.order_id, None)
                if order is not None and order.shop:
                    service_item.shop = order.shop

        return service_item_list

class OrderItemServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询订单详情列表"""

        order_item_qs = OrderItem.query(**search_info)

        return order_item_qs

    @classmethod
    def hung_item_fororder(cls, order):
        """订单挂载订单详情"""

        order.items = cls.search(order = order)

        return order

    @classmethod
    def hung_item_fororders(cls, order_list):
        """批量订单挂载订单详情"""
        order_mapping = {}
        for order in order_list:
            order_mapping[order.id] = order
            order_mapping[order.id].items = []
        order_item_list = OrderItem.search(order_id__in = order_mapping.keys())
        for order_item in order_item_list:
            if order_item.order.id in order_mapping:
                order_mapping[order_item.order.id].items.append(order_item)

        return order_list
