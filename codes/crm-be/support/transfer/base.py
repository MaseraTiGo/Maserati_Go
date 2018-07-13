# coding=UTF-8

import init_envt
import pymysql

from model.store.model_user import Staff
from model.store.model_staff_alias import StaffAlias


class BaseTransfer():

    def _init(self):
        self._conn = pymysql.connect(host = '192.168.3.112', port = 3306, user = 'root', passwd = 'root', db = 'bqcode', charset = 'utf8')
        self._cursor = self._conn.cursor(cursor = pymysql.cursors.DictCursor)

    def check_conn(self):
        if not hasattr(self, '_conn'):
            self._init()

    def get_date_list(self, sql_str):
        self.check_conn()
        self._cursor.execute(sql_str)
        data_list = self._cursor.fetchall()
        return data_list

    def break_link(self):
        self._cursor.close()
        self._conn.close()


    def get_staff_byname(self, staff_name):
        staff = None
        if staff_name:
            staff_alias_qs = StaffAlias.search(alias = staff_name.strip())
            if staff_alias_qs.count()>0:
                staff = staff_alias_qs[0].staff
            else:
                staff_name = self.format_str(staff_name)
                staff = Staff.get_staff_byname(staff_name)
                if staff is None:
                    staff = Staff.create(name = staff_name, is_working = False)

        return staff

    def is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def format_str(self, content):
        content_str = ''
        for i in content:
            if self.is_chinese(i):
                content_str = content_str + i
        return content_str
