# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.sys.utils.common.dictwrapper import DictWrapper

from model.models import Service, ServiceItem


class ServiceServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询服务列表"""
        user_pro = search_info.pop('cur_user')
        service_qs = Service.search(**search_info)
        if not user_pro._is_show_sub:
            service_qs = service_qs.filter(seller_id__exact = user_pro._cur_user_id)
        if user_pro._is_admin:
            service_qs = Service.query()
        service_qs = service_qs.order_by("-create_time")
        return Splitor(current_page, service_qs)

    @classmethod
    def get(cls, service_id):
        """售后服务单信息"""
        service = Service.get_byid(service_id)
        if service is None:
            raise BusinessError("售后服务单不存在")

        return service

    @classmethod
    def hung_staff_forservice(cls, service_item_list):
        """售后服务单产品挂在客服"""
        service_id_list = []
        for service_item in service_item_list:
            if service_item.service:
                service_id_list.append(service_item.service.id)

        service_mapping = {}
        if len(service_id_list) > 0:
            service_mapping = { service.id: service for service in \
                    Service.search(id__in = service_id_list)}

        for service_item in service_item_list:
            service_item.pre_staff = None
            service_item.after_staff = None
            service_item.order = None
            if service_item.service:
                service = service_mapping.get(service_item.service.id, None)
                if service is not None:
                    service_item.pre_staff = service.seller
                    service_item.after_staff = service.server
                    service_item.order = service.order

        return service_item_list


class ServiceItemServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """售后服务单产品列表查询"""

        if "equipment_code" in search_info:
            equipment_code = search_info.pop("equipment_code")
            search_info.update({"equipment__code":equipment_code})

        if "seller_staff_id" in search_info:
            seller_staff_id = search_info.pop("seller_staff_id")
            search_info.update({"service__seller_id":seller_staff_id})

        if "server_staff_id" in search_info:
            server_staff_id = search_info.pop("server_staff_id")
            search_info.update({"service__server_id":server_staff_id})

        if "shop_id" in search_info:
            shop_id = search_info.pop("shop_id")
            search_info.update({"order__shop_id":shop_id})

        if "buy_date_start" in search_info:
            buy_date_start = search_info.pop("buy_date_start")
            search_info.update({"order__pay_time__gte":buy_date_start})

        if "buy_date_end" in search_info:
            buy_date_end = search_info.pop("buy_date_end")
            search_info.update({"order__pay_time__lte":\
                                datetime.datetime(buy_date_end.year, buy_date_end.month, buy_date_end.day, 23, 59, 59)})

        service_item_qs = cls.search_qs(**search_info)
        service_item_qs = service_item_qs.order_by("-create_time")

        return Splitor(current_page, service_item_qs)

    @classmethod
    def search_qs(cls, **search_info):
        service_item_qs = ServiceItem.search(**search_info)
        return service_item_qs;

    @classmethod
    def get(cls, service_item_id):
        """售后服务单产品信息"""
        service_item = ServiceItem.get_byid(service_item_id)
        if service_item is None:
            raise BusinessError("售后服务单设备不存在")

        return service_item

    @classmethod
    def summing(cls, sum_data, **search_info):

        sum_measure_data = DictWrapper({})

        sum_measure_data.volume_total = 0
        sum_measure_data.open_number_total = 0
        sum_measure_data.activation_number_total = 0
        sum_measure_data.conversion_rate_total = "0%"
        sum_measure_data.open_rate_total = "0%"
        sum_measure_data.activation_rate_total = "0%"


        if 'cur_user' in search_info:
            user_pro = search_info.pop('cur_user')
            if not user_pro._is_admin:
                search_info.update({"service__seller_id__in": user_pro._staff_id_list})
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"order__pay_time__gte":\
                                datetime.datetime(begin_time.year, begin_time.month, begin_time.day, 0, 0, 0)})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"order__pay_time__lte":\
                                datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)})
        if "staff__in" in search_info:
            staff_list = search_info.pop("staff__in")
            search_info.update({"service__seller__in":staff_list})
        service_item_qs = cls.search_qs(**search_info)
        sum_measure_data.volume_total = service_item_qs.count()
        for service_item in service_item_qs:
            if service_item.dsinfo_status != "red":
                sum_measure_data.open_number_total += 1
            if service_item.rebate_status != "red":
                sum_measure_data.activation_number_total += 1

        if sum_data.new_number > 0 and sum_measure_data.volume_total > 0:
            sum_measure_data.conversion_rate_total = "{number}%".format(number = round((sum_measure_data.volume_total \
                                                / sum_data.new_number) * 100, 2))
        if sum_measure_data.volume_total > 0 and sum_measure_data.open_number_total > 0:
            sum_measure_data.open_rate_total = "{number}%".format(number = round((sum_measure_data.open_number_total \
                                                        / sum_measure_data.volume_total) * 100, 2))
        if sum_measure_data.volume_total > 0 and sum_measure_data.activation_number_total > 0:
            sum_measure_data.activation_rate_total = "{number}%".format(number = round((sum_measure_data.activation_number_total \
                                                                    / sum_measure_data.volume_total) * 100, 2))

        return sum_measure_data

    @classmethod
    def huang_serviceitem_rate(cls, measure_staff_list):
        """售后服务单产品挂载开通率激活率"""

        for measure_staff in measure_staff_list:

            measure_staff.volume = 0
            measure_staff.conversion_rate = "0%"
            measure_staff.open_number = 0
            measure_staff.open_rate = "0%"
            measure_staff.activation_number = 0
            measure_staff.activation_rate = "0%"

            if measure_staff.report_date:
                report_date = measure_staff.report_date
                report_date_min = datetime.datetime(report_date.year, report_date.month, report_date.day, 0, 0, 0)
                report_date_max = datetime.datetime(report_date.year, report_date.month, report_date.day, 23, 59, 59)
                service_item_qs = cls.search_qs(order__pay_time__gte = report_date_min, \
                                                order__pay_time__lte = report_date_max, \
                                                service__seller = measure_staff.staff)
                if service_item_qs.count() > 0:
                    measure_staff.volume = service_item_qs.count()
                    for service_item in service_item_qs:
                       if service_item.dsinfo_status != "red":
                            measure_staff.open_number += 1
                       if service_item.rebate_status != "red":
                            measure_staff.activation_number += 1

                    if measure_staff.new_number > 0 and measure_staff.volume > 0:
                        measure_staff.conversion_rate = "{number}%".format(number = round((measure_staff.volume \
                                                            / measure_staff.new_number) * 100, 2))
                    if measure_staff.volume > 0 and measure_staff.open_number > 0:
                        measure_staff.open_rate = "{number}%".format(number = round((measure_staff.open_number \
                                                                    / measure_staff.volume) * 100, 2))
                        measure_staff.activation_rate = "{number}%".format(number = round((measure_staff.activation_number \
                                                                    / measure_staff.volume) * 100, 2))
        return measure_staff_list

    @classmethod
    def Statistics(cls, measure_staff_mapping, service_item_list):

        for service_item in service_item_list:

            create_time_str = str(service_item.order.pay_time.date())
            temp_item = measure_staff_mapping[create_time_str]

            temp_item["volume"] += 1
            if service_item.dsinfo_status != "red" :
                temp_item["open_number"] += 1
            if service_item.rebate_status != "red" :
                temp_item["activation_number"] += 1

        statistics_list = []

        for measure_staff_mapping_item in measure_staff_mapping:
            temp_measure_item = measure_staff_mapping[measure_staff_mapping_item]
            if temp_measure_item["exhale_number"] > 0 and temp_measure_item["call_number"] > 0:
                temp_measure_item["call_rate"] = "{number}%".format(number = round((temp_measure_item["call_number"] \
                                                            / temp_measure_item["exhale_number"]) * 100, 2))

            if temp_measure_item["new_number"] > 0 and temp_measure_item["volume"] > 0:
                temp_measure_item["conversion_rate"] = "{number}%".format(number = round((temp_measure_item["volume"] \
                                                            / temp_measure_item["new_number"]) * 100, 2))
            if temp_measure_item["volume"] > 0 and temp_measure_item["open_number"] > 0:
                temp_measure_item["open_rate"] = "{number}%".format(number = round((temp_measure_item["open_number"] \
                                                            / temp_measure_item["volume"]) * 100, 2))
                temp_measure_item["activation_rate"] = "{number}%".format(number = round((temp_measure_item["activation_number"] \
                                                            / temp_measure_item["volume"]) * 100, 2))

            temp_measure_item["calculation_date"] = measure_staff_mapping_item

            statistics_list.append(temp_measure_item)

        return statistics_list

    @classmethod
    def get_serviceitem_byequipment(cls, equipment):
        service_item_qs = cls.search_qs(equipment = equipment)
        if service_item_qs.count() > 0:
            return service_item_qs[0]

        return None

    @classmethod
    def update(cls, service_item, **attr):
        service_item.update(**attr)
