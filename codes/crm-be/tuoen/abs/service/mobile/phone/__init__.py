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

from model.store.model_mobilephone import Mobilephone
from model.store.model_mobilephone import MobileDevices

class MobilephoneHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机"""
        mobilephone = Mobilephone.create(**attrs)
        if mobilephone is None:
            raise BusinessError("手机添加失败")

        return mobilephone

    @classmethod
    def get(cls, mobile_phone_id):
        """查询手机信息"""
        mobilephone = Mobilephone.get_byid(mobile_phone_id)
        if mobilephone is None:
            raise BusinessError("此手机不存在")

        return mobilephone

    @classmethod
    def update(cls, mobilephone, **attrs):
        """修改手机信息"""
        mobilephone.update(**attrs)

        return mobilephone

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机列表"""
        phone_qs = cls.search_qs(**search_info)
        
        if 'keyword' in search_info:
            keyword = search_info.pop('keyword')
            phone_qs = phone_qs.filter(Q(name__contains = keyword) | \
                Q(phone_number__contains = keyword))
                
        if 'mobile_code' in search_info:            
            mobile_code = search_info.pop('mobile_code')
            phone_qs = phone_qs.filter(devices_id = mobile_code)
            
        phone_qs = phone_qs.order_by("-create_time")
        return Splitor(current_page, phone_qs)

    @classmethod
    def search_qs(cls, **search_info):
        """查询手机列表"""
        return Mobilephone.query(**search_info)

    @classmethod
    def remove(cls, mobile_phone_id):
        """删除手机"""

        mobilephone = Mobilephone.get_byid(mobile_phone_id)
        if mobilephone is None:
            raise BusinessError("此手机不存在")

        mobilephone.delete()
        return True

    @classmethod
    def is_phone_exist(cls, phone, mobilephone = None):
        """判断手机号是否存在"""

        mobilephone_qs = Mobilephone.query().filter(phone_number = phone)
        if mobilephone is not None:
            mobilephone_qs = mobilephone_qs.filter(~Q(id = mobilephone.id))

        if mobilephone_qs.count() > 0:
            raise BusinessError("该手机号已存在")

        return True
