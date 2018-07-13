# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_transaction import EquipmentTransaction
from model.store.model_import import ImportCustomerTransaction


class EquipmentTransactionTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_user_transaction"


    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            transaction_list = self.generate_date(data_list)
            EquipmentTransaction.objects.bulk_create(transaction_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束==================")

    def generate_date(self, data_list):
        transaction_list = []
        import_transaction_list = []
        customer_ids = []
        customer_ids = [dic_data["customer_id"] for dic_data in data_list]

        register_mapping = {equipment_register.code:equipment_register for equipment_register in \
                          EquipmentRegister.search(code__in = customer_ids)}

        for dic_data in data_list:
            register = register_mapping.get(dic_data["customer_id"], None)
            if register is None:
                import_transaction_list.append(ImportCustomerTransaction(agent_name = dic_data["username"], service_code = dic_data["service_id"], \
                                                         code = dic_data["customer_id"], phone = dic_data["mobile"], \
                                                         transaction_year = datetime.datetime(dic_data["transaction_date"].year, dic_data["transaction_date"].month, dic_data["transaction_date"].day) \
                                                         if dic_data["transaction_date"] else None, \
                                                         transaction_day = dic_data["transaction_date"], \
                                                         transaction_code = dic_data["transaction_id"], \
                                                         transaction_money = int(dic_data["total_money"] * 100) if dic_data["total_money"] else 0, \
                                                         fee = int(dic_data["total_brokerage"] * 100) if dic_data["total_brokerage"] else 0, \
                                                         rate = int(dic_data["rate"] * 100) if dic_data["rate"] else 0, \
                                                         other_fee = int(dic_data["other_brokerage"] * 100) if dic_data["other_brokerage"] else 0, \
                                                         transaction_status = dic_data["status"], \
                                                         update_time = dic_data["modify_date"], create_time = dic_data["create_date"], \
                                                         status = "failed", error_text = "客户编码无法匹配"))
            else:
                transaction_list.append(EquipmentTransaction(agent_name = dic_data["username"], service_code = dic_data["service_id"], \
                                                             code = register, phone = dic_data["mobile"], transaction_time = dic_data["transaction_date"], \
                                                             transaction_code = dic_data["transaction_id"], \
                                                             transaction_money = int(dic_data["total_money"] * 100) if dic_data["total_money"] else 0, \
                                                             fee = int(dic_data["total_brokerage"] * 100) if dic_data["total_brokerage"] else 0, \
                                                             rate = int(dic_data["rate"] * 100) if dic_data["rate"] else 0, \
                                                             other_fee = int(dic_data["other_brokerage"] * 100) if dic_data["other_brokerage"] else 0, \
                                                             transaction_status = dic_data["status"], \
                                                             update_time = dic_data["modify_date"], create_time = dic_data["create_date"], \
                                                             ))


        return transaction_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)
