#coding=utf-8

'''
created on 20180608
@author: djd
'''

from tuoen.abs.middleware.role import role_middleware

from model.models import Staff
from model.models import AuthAccess
from model.models import Role

class UserRightServer(object):
    """用户权限控制"""
    _staff_qs = None
    _is_admin = False
    _staff_id_list = None
    _is_show_sub = True
    _cur_user_id = 0

    def __init__(self, cur_user):
        self._cur_user_id = cur_user.id
        if cur_user.is_admin:
            self._is_admin = True            
            self._staff_qs = Staff.query()
            self._staff_id_list = [s.id for s in self._staff_qs]
        else:
            all_sub_ids = []
            role_id_list = [ac.access_id for ac in AuthAccess.query().filter(staff=cur_user, access_type='role')] #Generator will not work, why?
            dept_id_list = (ac.access_id for ac in AuthAccess.query().filter(staff=cur_user, access_type='department'))
            for role_id in role_id_list:
                sub_list = role_middleware.get_all_children_ids(role_id)
                self._is_show_sub = any([role.is_show_data for role in Role.query().filter(id__in = sub_list)][:-1])
                if sub_list and self._is_show_sub:
                    all_sub_ids.extend(sub_list)
            role_id_list = [acs.staff_id for acs in \
                                AuthAccess.query().filter(access_id__in = all_sub_ids, access_type='role')
                              ]
            dept_id_list = [acs.staff_id for acs in \
                                AuthAccess.query().filter(access_id__in = dept_id_list, access_type='department')
                              ]                 
            staff_id_list = list(set(role_id_list).intersection(set(dept_id_list)))
            staff_id_list.append(cur_user.id)
            self._staff_id_list = staff_id_list
            self._staff_qs = Staff.query().filter(id__in = staff_id_list)
