# coding=UTF-8

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField
from model.store.model_import import ImportCustomerRebate
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_service import ServiceItem
from model.store.model_equipment import EquipmentStatusType


class RebateImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""
        self._equipment_register = None

    def get_exec_cls(self):
        return ImportCustomerRebate

    def get_fields(self):
        check_list = [
            ['agent_id', CharField(desc = "代理商ID")],
            ['agent_name', CharField(desc = "代理商名称")],
            ['code', CharField(desc = "客户编码")],
            ['name', CharField(desc = "客户名称")],
            ['phone', CharField(desc = "注册手机号")],
            ['activity_type', CharField(desc = "活动类型")],
            ['device_code', CharField(desc = "设备编码")],
            ['register_time', ExcelDateTimeField(desc = "注册时间")],
            ['bind_time', ExcelDateTimeField(desc = "绑定时间")],
            ['month', ExcelDateTimeField(desc = "交易月份")],
            ['transaction_amount', ExcelMoneyField(desc = "交易金额/分")],
            ['effective_amount', ExcelMoneyField(desc = "有效金额/分")],
            ['accumulate_amount', ExcelMoneyField(desc = "当月累计交易金额/分")],
            ['history_amount', ExcelMoneyField(desc = "历史累计交易金额/分")],
            ['type', CharField(desc = "号段类型")],
            ['is_rebate', CharField(desc = "是否返利")],
            ['remark', CharField(desc = "备注")],
        ]
        return check_list

    def skip_repeat(self, code, month):
        equipment_register_qs = EquipmentRegister.query().filter(code = code)
        if equipment_register_qs.count() == 0:
            self._error_msg = "客户id不存在"
            return False

        self._equipment_register = equipment_register_qs[0]
        equipment_rebate_qs = EquipmentRebate.query(code = self._equipment_register, month = month)
        if equipment_rebate_qs.count() > 0:
            self._error_msg = "数据重复"
            return False


        return True

    def exec_convet(self, rebate):
        check_repeat = self.skip_repeat(rebate.code, rebate.month)
        if check_repeat:
            service_item_qs = ServiceItem.query(equipment = self._equipment_register.equipment)
            if service_item_qs.count() > 0:
                EquipmentRebate.create(agent_id = rebate.agent_id, agent_name = rebate.agent_name, \
                                       code = self._equipment_register, name = rebate.name, phone = rebate.phone, \
                                       activity_type = rebate.activity_type, register_time = rebate.register_time, \
                                       bind_time = rebate.bind_time, month = rebate.month, transaction_amount = rebate.transaction_amount, \
                                       effective_amount = rebate.effective_amount, accumulate_amount = rebate.accumulate_amount, \
                                       history_amount = rebate.history_amount, type = rebate.type, is_rebate = rebate.is_rebate, \
                                       remark = rebate.remark, register_code = rebate.code);
                if "已达到" in rebate.remark:
                    service_item = service_item_qs[0]
                    if service_item.rebate_status == EquipmentStatusType.GREEN:
                        service_item.update(rebate_status = EquipmentStatusType.TGREEB)
                return True, ""

        return False, self._error_msg
