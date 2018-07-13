# coding=UTF-8

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField
from model.store.model_import import ImportCustomerRegister
from model.store.model_equipment import Equipment, EquipmentStatusType
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import ServiceItem

class RegisterImport(ExcelImport):
    
    def __init__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportCustomerRegister

    def get_fields(self):
        check_list = [
            ['agent_name', CharField(desc = "代理商名称")],
            ['code', CharField(desc = "客户编码")],
            ['phone', CharField(desc = "注册手机号")],
            ['name', CharField(desc = "客户姓名")],
            ['register_time', ExcelDateTimeField(desc = "客户注册时间")],
            ['bind_time', ExcelDateTimeField(desc = "绑定时间")],
            ['device_code', CharField(desc = "设备编码")],
        ]
        return check_list

    def skip_repeat(self, register):
        equipment_register_qs = EquipmentRegister.query().filter(code = register.code)
        if equipment_register_qs.count() > 0:
            self._error_msg = "客户编码重复"
            return False

        return True

    def exec_convet(self, register):
        check_repeat = self.skip_repeat(register)
        if check_repeat:
            equipment_qs = Equipment.query().filter(code = register.device_code)
            if equipment_qs.count() > 0:
                equipment = equipment_qs[0]
                equipment_register = EquipmentRegister.create(equipment = equipment, agent_name = register.agent_name, \
                                         code = register.code, phone = register.phone, name = register.name, \
                                         register_time = register.register_time, bind_time = register.bind_time, \
                                         device_code = register.device_code)
                service_item = ServiceItem.query(equipment = equipment)[0]
                service_item.update(dsinfo_status = EquipmentStatusType.YELLOW)
                return True, ""
            else:
                self._error_msg = "此设备SN码系统不存在"

        return False, self._error_msg
