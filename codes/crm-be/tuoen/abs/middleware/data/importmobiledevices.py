# coding=UTF-8
import hashlib

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportMobileDevices
from model.store.model_mobilephone import MobileDevices, Mobilephone, MobileDeviceStatus, MobileMaintain
from model.store.model_user import Staff


class MobileDevicesImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportMobileDevices

    def get_fields(self):
        check_list = [
            ['group_leader', CharField(desc = "组长姓名")],
            ['mobile_code', ExcelDeletePointField(desc = "手机编号")],
            ['group_member', CharField(desc = "组员姓名")],
            ['wechat_nick', CharField(desc = "微信昵称")],
            ['wechat_number', CharField(desc = "微信号")],
            ['wechat_password', CharField(desc = "微信密码")],
            ['pay_password', ExcelDeletePointField(desc = "微信支付密码")],
            ['wechat_remark', CharField(desc = "微信号备注")],
            ['department', CharField(desc = "部门")],
            ['phone_number', ExcelDeletePointField(desc = "手机号")],
            ['operator', CharField(desc = "运营商")],
            ['real_name', CharField(desc = "实名人姓名")],
            ['phone_remark', CharField(desc = "手机号备注")],
            ['flow_card_number', CharField(desc = "流量卡号")],
            ['imei', CharField(desc = "手机imei号")],
            ['brand', CharField(desc = "手机品牌")],
            ['model', CharField(desc = "手机型号")],
            ['price', ExcelMoneyField(desc = "购买价格/分")],
            ['mobile_status', CharField(desc = "手机设备状态")],
            ['mobile_remark', CharField(desc = "手机设备备注")],
            ['phone_change', CharField(desc = "手机变更信息")],
        ]
        return check_list


    def skip_mobile_devices(self, mobile_code):
        if not mobile_code:
            self._error_msg = "缺少手机编号"
            return False

        mobile_devices_qs = MobileDevices.search(code = mobile_code)
        if mobile_devices_qs.count() > 0:
            self._error_msg = "重复数据"
            return False

        return True

    def exec_convet(self, mobile_devices):
        check_mobile_devices = self.skip_mobile_devices(mobile_devices.mobile_code)
        if check_mobile_devices:
            devices = MobileDevices.create(code = mobile_devices.mobile_code, brand = mobile_devices.brand, \
                                                  model = mobile_devices.model, price = mobile_devices.price, \
                                                  status = self.get_devices_status(mobile_devices.mobile_status), \
                                                  remark = self.get_mobile_devices_remark(mobile_devices.mobile_remark, mobile_devices.department), \
                                                  imei = mobile_devices.imei, \
                                                  )
            mobile_phone_staff = self.get_staff(mobile_devices.real_name)

            mobile_phone = self.get_mobile_phone(mobile_devices.phone_number)
            if mobile_phone is None:
                Mobilephone.create(devices = devices, staff = mobile_phone_staff, name = mobile_devices.real_name, \
                                   identity = mobile_phone_staff.identity if mobile_phone_staff else "", wechat_nick = mobile_devices.wechat_nick, \
                                   wechat_number = mobile_devices.wechat_number, wechat_password = mobile_devices.wechat_password, \
                                   pay_password = mobile_devices.pay_password, wechat_remark = mobile_devices.wechat_remark, \
                                   phone_number = mobile_devices.phone_number, operator = mobile_devices.operator, \
                                   phone_remark = mobile_devices.phone_remark, flow_card_number = mobile_devices.flow_card_number, \
                                   )
            else:
                mobile_phone.update(devices = devices, staff = mobile_phone_staff, name = mobile_devices.real_name, \
                                   identity = mobile_phone_staff.identity if mobile_phone_staff else "", wechat_nick = mobile_devices.wechat_nick, \
                                   wechat_number = mobile_devices.wechat_number, wechat_password = mobile_devices.wechat_password, \
                                   pay_password = mobile_devices.pay_password, wechat_remark = mobile_devices.wechat_remark, \
                                   phone_number = mobile_devices.phone_number, operator = mobile_devices.operator, \
                                   phone_remark = mobile_devices.phone_remark, flow_card_number = mobile_devices.flow_card_number, \
                                   )

            mobile_maintain_staff = self.get_staff(mobile_devices.group_member)
            if mobile_maintain_staff is not None:
                MobileMaintain.create(devices = devices, staff = mobile_maintain_staff, \
                                      remark = self.get_mobile_maintain_remark(mobile_devices.group_leader))
            return True, ""

        return False, self._error_msg

    def get_mobile_phone(self, phone_number):
        mobile_phone = None
        mobile_phone_qs = Mobilephone.query().filter(phone_number = phone_number)
        if mobile_phone_qs.count() > 0:
            mobile_phone = mobile_phone_qs[0]

        return mobile_phone

    def get_devices_status(self, mobile_status):
        switch = {
            "正常":MobileDeviceStatus.NORMAL,
            "报废":MobileDeviceStatus.SCRAP,
            "闲置":MobileDeviceStatus.IDLE,
            "其它":MobileDeviceStatus.OTHER,
        }
        try:
            return switch[mobile_status]
        except Exception as e:
            return MobileDeviceStatus.OTHER


    def get_staff(self, staff_name):
        staff = Staff.get_staff_byname(staff_name)

        return staff

    def get_mobile_devices_remark(self, mobile_remark, department):
        if not department:
            return "{a}({b})".format(a = mobile_remark, b = department)

        return mobile_remark

    def get_mobile_maintain_remark(self, group_leader):
        if not group_leader:
            return "组长为:({a})".format(a = group_leader)

        return ""
