# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff

class AccessTypes(object):
    ROLE = "role"
    DEPARTMENT = "department"
    CHOICES = ((ROLE, '角色'), (DEPARTMENT, "部门"))


class AuthAccess(BaseModel):
    staff = ForeignKey(Staff)
    access_id = IntegerField(verbose_name = "对应角色或者部门id", default = 0)
    access_type = CharField(verbose_name = "对应类型", max_length = 128, choices = AccessTypes.CHOICES, default = AccessTypes.ROLE)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def get_by_access_id(cls, access_id, access_type):
        """根据access_id查询关系信息"""

        access_list = cls.query(access_id = access_id, access_type = access_type)
        return access_list

    @classmethod
    def search(cls, **attrs):
        access_qs = cls.query().filter(**attrs)
        return access_qs
