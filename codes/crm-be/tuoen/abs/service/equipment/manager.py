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

from tuoen.abs.service.equipment.register import EquipmentRegisterHelper

from model.models import Equipment



class EquipmentServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询设备列表"""

        equipment_qs = Equipment.search(**search_info)

        equipment_qs.order_by("-create_time")
        return Splitor(current_page, equipment_qs)

    @classmethod
    def hung_code_bylogistics(cls, logistics_list):
        """根据物流详情挂载设备"""
        for logistics in logistics_list:
            for logisticsitem in logistics.items:
                equipment_qs = Equipment.search(logistics_item = logisticsitem)
                logisticsitem.equipment_list = equipment_qs

        return logistics_list

class EquipmentRegisterServer(object):

    @classmethod
    def get(cls, id):
        """查询设备注册信息"""
        return EquipmentRegisterHelper.get(id)

    @classmethod
    def update(cls, equipment_register, **attrs):
        """修改设备注册信息"""
        return EquipmentRegisterHelper.update(equipment_register, **attrs)

    @classmethod
    def get_register_byequipment(cls, equipment):
        """根据设备查询注册信息"""
        return EquipmentRegisterHelper.get_register_byequipment(equipment)

