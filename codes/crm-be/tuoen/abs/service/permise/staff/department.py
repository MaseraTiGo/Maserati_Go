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

from model.models import Department, AuthAccess

from tuoen.abs.middleware.department import department_middleware


class DepartmentHelper(object):
    
    @classmethod
    def generate(cls, **department_info):
        """创建部门"""
        
        department = Department.create(**department_info)
        if department is None:
            raise BusinessError("部门创建失败")
        
        department_middleware.force_refresh()
        return department
        
    @classmethod
    def search(cls, **attrs):
        """查询部门列表"""
        department_list = Department.search(**attrs)
        return department_list
    
    @classmethod
    def get(cls, department_id):
        """获取部门详情"""
        department = Department.get_byid(department_id)
        if department is None:
            raise BusinessError("该部门不存在")
        return department 
    
    @classmethod
    def update(cls, department, **attrs):
        """编辑部门"""
        department.update(**attrs)
        department_middleware.force_refresh()
        
        return True
    
    @classmethod
    def remove(cls, department_id):
        """删除部门"""
        
        access_type = "department"
        auth_access = AuthAccess.get_by_access_id(department_id, access_type)
        if auth_access.count() > 0:
            raise BusinessError("已绑定用户无法删除")
        
        department_children = department_middleware.get_children(department_id)
        if department_children:
            raise BusinessError("此部门存在下级无法删除")
        
        department = Department.get_byid(department_id)
        if department is None:
            raise BusinessError("该部门不存在")
               
        department.delete()
        
        department_middleware.force_refresh()
        
        return True
    
    @classmethod
    def is_exit(cls, department_id):
        """判断该角色是否存在"""
        department = Department.get_byid(department_id)
        if department is None:
            return False
        return True 

    @classmethod
    def is_name_exist(cls, name, department = None):
        """判断部门名称是否存在"""
        department_qs = Department.search(name = name)

        if department is not None:
            department_qs = department_qs.filter(~Q(id = department.id))

        if department_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True
