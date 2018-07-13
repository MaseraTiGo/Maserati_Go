# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_measure_staff import MeasureStaff
from model.store.model_user import Staff


class MeasureStaffTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select a.create_date,a.modify_date,a.report_date,a.data_number,a.exhale_number,a.call_number,a.call_rate,a.wechat_number,\
            a.volume,a.conversion_rate,b.name as staff_name,c.name as record_name from ct_reports a left join ct_admin b ON a.customer=b.id left join ct_admin c ON \
            a.recordid=c.id"

    def run(self):
        print("进入")
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            measure_staff_list = self.generate_date(data_list)
            MeasureStaff.objects.bulk_create(measure_staff_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束MeasureStaff==================")

    def generate_date(self, data_list):
        measure_staff_list = []
        for dic_data in data_list:
            measure_staff_list.append(MeasureStaff(staff = self.get_staff_byname(dic_data["staff_name"]), \
                                                 record = self.get_staff_byname(dic_data["record_name"]), new_number = dic_data["data_number"], \
                                                 exhale_number = dic_data["exhale_number"], call_number = dic_data["call_number"], \
                                                 wechat_number = dic_data["wechat_number"], report_date = dic_data["report_date"], \
                                                 update_time = dic_data["modify_date"], create_time = dic_data["create_date"]))

        return measure_staff_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)
