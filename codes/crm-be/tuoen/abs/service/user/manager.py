# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import Q

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.abs.service.user.token import Token
from tuoen.abs.middleware.role import role_middleware

from model.models import Staff
from model.models import AuthAccess
from model.models import Role
from model.models import Department
from model.models import AuthAccess

class UserServer(object):

    @classmethod
    def generate_token(cls, user):
        return Token.generate(user.id, user.__class__.__name__)

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        token = Token.get(auth_str)
        token.renew(renew_str)
        return token

    @classmethod
    def get_token(cls, auth_str, parms = None):
        token = Token.get(auth_str)
        token.check(parms)
        return token


class StaffServer(object):

    @classmethod
    def register(cls, **attrs):
        """添加员工"""
        staff = Staff.create(**attrs)
        if staff is None:
            raise BusinessError("员工添加失败")
        return staff

    @classmethod
    def get(cls, staff_id):
        """获取员工个人信息"""
        staff = Staff.get_byid(staff_id)
        if staff is None:
            raise BusinessError("员工不存在")
        return staff

    @classmethod
    def update(cls, staff, **attrs):
        """修改员工个人信息"""
        staff.update(**attrs)
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        """查询员工列表"""
        user_pro = search_info.pop('cur_user')
        staff_qs = user_pro._staff_qs        
        if 'keyword' in search_info:
            keyword = search_info.pop('keyword')
            staff_qs = staff_qs.filter(Q(name__contains = keyword) | \
                            Q(phone__contains = keyword))
        dept_staff_id = []                    
        role_staff_id = []
        d_flag = False
        r_flag = False
        if 'department' in search_info:
            d_flag = True
            dept_id = search_info.pop('department')
            #dept_id = [d.id for d in Department.query().filter(name__contains = dept)] #使用名称查找
            dept_staff_id = [a.staff_id for a in AuthAccess.query().filter(access_id__exact = dept_id, access_type = 'department')]
        if 'role' in search_info:
            r_flag = True
            role_id = search_info.pop('role')
            #role_id = [r.id for r in Role.query().filter(name__contains = role)] #使用名称查找
            role_staff_id = [a.staff_id for a in AuthAccess.query().filter(access_id__exact = role_id, access_type = 'role')]
        if all((d_flag, r_flag)):
            staff_id_list = list(set(role_staff_id).intersection(set(dept_staff_id)))
            staff_qs = staff_qs.filter(id__in = staff_id_list)
        elif not d_flag and not r_flag:
            pass
        else:
            staff_id_list = dept_staff_id + role_staff_id
            staff_qs = staff_qs.filter(id__in = staff_id_list)
        if 'is_working' in search_info:
            is_working = search_info.pop('is_working')
            staff_qs = staff_qs.filter(is_working = is_working)
        staff_qs = staff_qs.order_by("-entry_time")
        return Splitor(current_page, staff_qs)

    @classmethod
    def search_all(cls, **search_info):
        """查询所有员工列表"""
        staff_qs = Staff.search(**search_info)
        staff_qs = staff_qs.order_by("-create_time")

        return staff_qs

    @classmethod
    def match(cls, keyword, size = 5):
        """查询员工列表"""
        return Staff.query(name = keyword).order_by('-create_time')[:size]

    @classmethod
    def get_staff_byname(cls, name):
        """根据姓名查询员工"""
        staff = Staff.get_staff_byname(name = name)
        return staff

    @classmethod
    def is_name_exist(cls, name):
        """判断员工姓名是否存在"""

        staff = cls.get_staff_byname(name = name)

        if staff is not None:
            raise BusinessError("该名称已存在")
        return True

    @classmethod
    def check_exist(cls, identity, staff = None):
        """判断身份证号是否存在"""

        staff_identity_qs = Staff.query(identity = identity)
        if staff is not None:
            staff_identity_qs = staff_identity_qs.filter(~Q(id = staff.id))
        if staff_identity_qs.count() > 0:
            raise BusinessError("该身份证号已存在")

        return True

    @classmethod
    def judge_staff_role(cls, admin):
        """判断员工是否为管理员"""
        if not admin.is_admin:
            raise BusinessError("当前身份不为管理员")
        return True
