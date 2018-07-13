# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_equipment import Equipment
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import ServiceItem


class EquipmentRegisterTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select create_date,modify_date,name,register_id,terminal_code,sn_color,\
            agent_name,customer_code,customer_createtime,customer_bindtime,rebate_color from ct_channel_user where is_dsinfo=1"

    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            self.generate_date(data_list)
            # EquipmentRegister.objects.bulk_create(register_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束==================")

    def generate_date(self, data_list):
        for dic_data in data_list:
            if self.skip_register(dic_data["terminal_code"]):
                equipment = Equipment.create(code = dic_data["terminal_code"])
                EquipmentRegister.create(equipment = equipment, name = dic_data["name"], code = dic_data["customer_code"], \
                                         phone = dic_data["register_id"], agent_name = dic_data["agent_name"], \
                                         register_time = dic_data["customer_createtime"], \
                                         bind_time = dic_data["customer_bindtime"], \
                                         update_time = dic_data["modify_date"], create_time = dic_data["create_date"])
                ServiceItem.create(equipment = equipment, dsinfo_status = "yellow", rebate_status = self.get_rebate_status(dic_data["rebate_color"]), sn_status = dic_data["sn_color"])


    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def skip_register(self, customer_code):
        equipment_register_qs = EquipmentRegister.search(code = customer_code)
        if equipment_register_qs.count() == 0:
            return True
        return False


    def get_rebate_status(self, sn_color):
        rebate_status = sn_color
        if sn_color == "green":
            rebate_status = "tgreen"
        elif sn_color == "green1":
            rebate_status = "green"

        return rebate_status
