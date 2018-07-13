# coding=UTF-8
import datetime

from tuoen.sys.utils.common.timetools import add_month

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportCustomerTransaction
from model.store.model_equipment import Equipment, EquipmentStatusType
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_transaction import EquipmentTransaction
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_service import ServiceItem


class TransactionImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""
        self._equipment_register = None

    def get_exec_cls(self):
        return ImportCustomerTransaction

    def get_fields(self):
        check_list = [
            ['agent_name', CharField(desc = "代理商名称")],
            ['service_code', CharField(desc = "服务编码")],
            ['code', CharField(desc = "客户编码")],
            ['phone', CharField(desc = "注册手机号")],
            ['transaction_year', ExcelDateTimeField(desc = "交易日期")],
            ['transaction_day', ExcelDeletePointField(desc = "交易时间")],
            ['transaction_code', CharField(desc = "交易流水号")],
            ['transaction_money', ExcelMoneyField(desc = "交易金额/分")],
            ['fee', ExcelMoneyField(desc = "手续费/分")],
            ['rate', ExcelMoneyField(desc = "客户费率/分")],
            ['other_fee', ExcelMoneyField(desc = "其它手续费/分")],
            ['transaction_status', CharField(desc = "交易状态")],
            ['type', CharField(desc = "号段类型")],
        ]
        return check_list

    def skip_repeat(self, code, transaction_time):
        equipment_register_qs = EquipmentRegister.query().filter(code = code)
        if equipment_register_qs.count() == 0:
            self._error_msg = "客户编码不存在"
            return False

        self._equipment_register = equipment_register_qs[0]
        equipment_transaction_qs = EquipmentTransaction.query(code = self._equipment_register, \
                                                              transaction_time = transaction_time)
        if equipment_transaction_qs.count() > 0:
            self._error_msg = "数据重复"
            return False

        return True

    def exec_convet(self, transaction):
        if transaction.transaction_status != "成功":
            self._error_msg = "交易失败无法转化"
            return False, self._error_msg
        try:
            transaction_time_str = "{y}{d}".format(y = transaction.transaction_year.strftime("%Y-%m-%d"), d = transaction.transaction_day)
            transaction_time = datetime.datetime.strptime(transaction_time_str, '%Y-%m-%d%H%M%S')
        except Exception as e:
            self._error_msg = "交易日期或时间错误"
            return False, self._error_msg

        check_repeat = self.skip_repeat(transaction.code, transaction_time)
        rebate_money = self.get_rebate_money(self._equipment_register.equipment_id)

        if rebate_money <= 0:
            self._error_msg = "激活返现金额异常，请联系管理员修改"
            return False, self._error_msg
        if check_repeat:
            service_item_qs = ServiceItem.query(equipment = self._equipment_register.equipment)
            if service_item_qs.count() > 0:
                equipment_transaction = EquipmentTransaction.create(agent_name = transaction.agent_name, service_code = transaction.service_code, \
                            code = self._equipment_register, phone = transaction.phone, transaction_time = transaction_time, \
                            transaction_code = transaction.transaction_code, transaction_money = transaction.transaction_money, \
                            fee = transaction.fee, rate = transaction.rate, other_fee = transaction.other_fee, \
                            transaction_status = transaction.transaction_status, type = transaction.type, register_code = transaction.code)
                service_item = service_item_qs[0]
                if service_item.rebate_status == EquipmentStatusType.RED:
                    last_time = add_month(self._equipment_register.bind_time, 2)
                    total_money_lastmonth = EquipmentTransaction.sum_money(transaction_time__range = (self._equipment_register.bind_time, last_time), \
                                                                           code = self._equipment_register)
                    if total_money_lastmonth > rebate_money:
                       equipment_rebate_qs = EquipmentRebate.query().filter(code = self._equipment_register, remark__contains = "已达到")
                       if equipment_rebate_qs.count() > 0:
                           service_item.update(rebate_status = EquipmentStatusType.TGREEB)
                       else:
                           service_item.update(rebate_status = EquipmentStatusType.GREEN)
                    else:
                        total_money = EquipmentTransaction.sum_money(code = self._equipment_register)
                        if total_money > rebate_money:
                            service_item.update(rebate_status = EquipmentStatusType.YELLOW)
                return True, ""

        return False, self._error_msg

    def get_rebate_money(self, equipment_id):
        if equipment_id:
            equipment = Equipment.get_byid(equipment_id)
            if equipment is not None:
                if equipment.product is not None:
                    return equipment.product.rebate_money

        return 0
