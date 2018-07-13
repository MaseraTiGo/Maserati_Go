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

from model.models import MeasureStaff

class MeasureStaffHelper(object):

    @classmethod
    def generate(cls, **measure_staff_info):
        """创建员工绩效"""

        measure_staff = MeasureStaff.create(**measure_staff_info)
        if measure_staff is None:
            raise BusinessError("员工绩效添加失败")

        return measure_staff

    @classmethod
    def search(cls, current_page, measure_staff_qs):
        """查询员工绩效列表"""

        measure_staff_qs = measure_staff_qs.order_by("-report_date")
        return Splitor(current_page, measure_staff_qs)

    @classmethod
    def search_qs(cls, **search_info):        
        if 'cur_user' in search_info:
            user_pro = search_info.pop('cur_user')
            if not user_pro._is_admin:
                search_info.update({"staff_id__in": user_pro._staff_id_list})
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"report_date__gte":begin_time})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"report_date__lte":end_time})
        measure_staff_qs = MeasureStaff.search(**search_info)
        return measure_staff_qs

    @classmethod
    def search_by_month(cls, **search_info):

        measure_staff_qs = MeasureStaff.search(**search_info)

        return measure_staff_qs

    @classmethod
    def get(cls, measure_staff_id):
        """获取员工绩效详情"""

        measure_staff = MeasureStaff.get_byid(measure_staff_id)
        if measure_staff is None:
            raise BusinessError("员工绩效不存在")
        return measure_staff


    @classmethod
    def update(cls, measure_staff_id, **attrs):
        """编辑员工绩效"""

        measure_staff = cls.get(measure_staff_id)
        if measure_staff is None:
            raise BusinessError("员工绩效不存在")

        measure_staff.update(**attrs)
        return True

    @classmethod
    def remove(cls, measure_staff_id):
        """移除员工绩效"""

        measure_staff = cls.get(measure_staff_id)
        measure_staff.delete()

        return True
