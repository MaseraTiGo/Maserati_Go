# coding=UTF-8
import re
import datetime
import json

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField
from model.store.model_import import ImportCustomerBuyinfo

from django.db.models import *

from model.store.model_user import Staff
from model.store.model_staff_alias import StaffAlias
from model.store.model_mobilephone import MobileDevices, MobileMaintain
from model.store.model_shop import Shop, Goods
from model.store.model_customer import Customer
from model.store.model_order import Order, StatusTypes, OrderItem
from model.store.model_customer_chance import SaleChance
from model.store.model_order_event import StaffOrderEvent
from model.store.model_logistics import Logistics, LogisticsItem
from model.store.model_equipment import Equipment, EquipmentStatusType
from model.store.model_service import Service, ServiceItem
from model.store.model_equipment_in import EquipmentIn
from model.store.model_equipment_out import EquipmentOut
from model.store.model_product import ProductModel
from model.store.model_measure_staff import MeasureStaff


class BuyinfoImport(ExcelImport):

    def __init__(self):
        self._staff = None
        self._server_staff = None
        self._mobiledevices = None
        self._shop = None
        self._equipment_in = None
        self._product_model = None
        self._device_code = ""
        self._error_msg = ""
        self._remark_pure = ""

    def get_exec_cls(self):
        return ImportCustomerBuyinfo

    def get_fields(self):
        check_list = [
            ['serial_number', IntField(desc = "序号")],
            ['order_sn', CharField(desc = "订单编号")],
            ['goods_sn', CharField(desc = "商品编号")],
            ['buy_number', IntField(desc = "购买数量")],
            ['buy_money', ExcelMoneyField(desc = "订单金额/分")],
            ['pay_time', ExcelDateTimeField(desc = "付款时间")],
            ['shop_name', CharField(desc = "网点名称")],
            ['buy_name', CharField(desc = "买家姓名")],
            ['province', CharField(desc = "省")],
            ['city', CharField(desc = "市")],
            ['area', CharField(desc = "区")],
            ['address', CharField(desc = "详细地址")],
            ['logistics_company', CharField(desc = "物流公司")],
            ['logistics_code', CharField(desc = "物流单号")],
            ['buy_phone', CharField(desc = "联系方式")],
            ['remark', CharField(desc = "客服备注")],
            ['buy_nick', CharField(desc = "卖家账号")],
            ['device_code', CharField(desc = "设备编码")],
        ]
        return check_list
    '''
    def exec_convet(self, buyinfo):
        check_integrity = self.check_data_integrity(buyinfo)
        if not check_integrity:
            return False
        check_repeat = self.skip_repeat(buyinfo.device_code)
        if check_repeat:

            buyinfo.device_code = device_code  # 待处理

            staff = None
            mobiledevices = None
            mobilemaintain = None
            server_staff = None
            if buyinfo.remark:
                staff_name, mobile_code, remark_pure = self.analysis_remark(buyinfo.remark)
                staff = self.convet_staff(staff_name)
                mobiledevices = self.convet_mobiledevices(mobile_code)
                if mobiledevices is not None:
                    mobilemaintain = self.convet_mobilemaintain(mobiledevices)
            else:
                remark_pure = ""
            shop = self.convet_shop(buyinfo.shop_name)
            customer = self.convet_customer(buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                            buyinfo.area, buyinfo.address, buyinfo.buy_phone, \
                                            buyinfo.buy_nick, mobiledevices = mobiledevices)
            goods, product_model = self.convet_goods(equipment_in, buyinfo.goods_sn, buyinfo.buy_number, buyinfo.buy_money, shop)
            order = self.convet_order(buyinfo.order_sn, buyinfo.buy_money, buyinfo.buy_number, \
                                      buyinfo.pay_time, buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                      buyinfo.area, buyinfo.address, buyinfo.buy_phone, customer, shop, remark_pure = remark_pure)
            if order is not None:
                order_item = OrderItem.create(order = order, goods = goods, name = buyinfo.goods_sn, \
                                              alias = buyinfo.goods_sn, price = buyinfo.buy_money, \
                                              quantity = buyinfo.buy_number)
                sale_chance = self.convet_sale_chance(staff, customer, shop, goods, buyinfo.pay_time, order)
                staff_order_event = StaffOrderEvent.create(staff = staff, order = order, remark = buyinfo.remark)
                logistics = Logistics.create(order = order, customer = customer, company = buyinfo.logistics_company, \
                                             number = buyinfo.logistics_code, total_quantity = buyinfo.buy_number)
                logistics_item = LogisticsItem.create(customer = customer, logistics = logistics, order_item = order_item, \
                                                    quantity = buyinfo.buy_number)
                equipment = Equipment.create(customer = customer, logistics_item = logistics_item, order = order, \
                                           code = buyinfo.device_code, product_model = product_model, product = product_model.product)
                if mobilemaintain is not None:
                    server_staff = mobilemaintain.staff
                service = Service.create(seller = staff, server = server_staff, customer = customer, order = order, \
                                         end_time = datetime.datetime.now() + datetime.timedelta(days = 5))
                service_item = ServiceItem.create(customer = customer, service = service, equipment = equipment, order = order, sn_status = EquipmentStatusType.GREEN)
            return True
        return False
    '''
    def exec_convet(self, buyinfo):

        check_integrity = self.check_data_integrity(buyinfo)

        if not check_integrity:
            return False, self._error_msg

        customer = self.convet_customer(buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                        buyinfo.area, buyinfo.address, buyinfo.buy_phone, \
                                        buyinfo.buy_nick)

        goods = self.convet_goods(buyinfo.goods_sn, buyinfo.buy_number, buyinfo.buy_money)

        order = self.convet_order(buyinfo.order_sn, buyinfo.buy_money, buyinfo.buy_number, \
                                  buyinfo.pay_time, buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                  buyinfo.area, buyinfo.address, buyinfo.buy_phone, customer)

        order_item = OrderItem.create(order = order, goods = goods, name = goods.name, \
                                              alias = goods.name, price = order.total_price, \
                                              quantity = order.total_quantity)

        sale_chance = self.convet_sale_chance(self._staff, customer, goods, order)

        staff_order_event = StaffOrderEvent.create(staff = self._staff, order = order, remark = self._remark_pure)

        logistics = Logistics.create(order = order, customer = customer, company = buyinfo.logistics_company, \
                                     number = buyinfo.logistics_code, total_quantity = order.total_quantity)

        logistics_item = LogisticsItem.create(customer = customer, logistics = logistics, order_item = order_item, \
                                              quantity = order.total_quantity)

        equipment = Equipment.create(customer = customer, logistics_item = logistics_item, order = order, \
                                     code = self._device_code, product_model = self._product_model, product = self._product_model.product)

        service = Service.create(seller = self._staff, server = self._server_staff, customer = customer, order = order, \
                                 end_time = datetime.datetime.now() + datetime.timedelta(days = 5))

        service_item = ServiceItem.create(customer = customer, service = service, equipment = equipment, order = order, sn_status = EquipmentStatusType.GREEN)
        
        if self._staff is not None:
            self.convet_measure_staff(self._staff, order.pay_time)

        return True, ""


    def general_measure_staff(self):

        pass

    def check_data_integrity(self, buyinfo):
        if not buyinfo.device_code:
            self._error_msg = "缺少设备编码"
            return False
        if not buyinfo.order_sn:
            self._error_msg = "缺少订单编号"
            return False,
        if not buyinfo.shop_name:
            self._error_msg = "缺少店铺名称"
            return False
        if not buyinfo.buy_name:
            self._error_msg = "缺少购买人姓名"
            return False
        if not buyinfo.buy_phone:
            self._error_msg = "缺少购买人联系方式"
            return False
        if not buyinfo.goods_sn:
            self._error_msg = "缺少商品编号"
            return False
        if not buyinfo.remark:
            self._error_msg = "缺少备注信息"
            return False

        check_repeat = self.skip_repeat(buyinfo.device_code)
        if not check_repeat:
            return False

        check_remark = self.analysis_remark(buyinfo.remark)
        if not check_remark:
            return False

        shop = Shop.get_shop_buyname(buyinfo.shop_name)
        if shop is None:
            self._error_msg = "该店铺系统不存在，请通知相关人员进行添加"
        else:
            self._shop = shop

        return True

    def handle_device_code(self, device_code):
        device_code = device_code.strip()
        device_code_len = len(device_code)
        if device_code_len == 19:
            device_code = device_code[4:]
        elif device_code_len == 20:
            device_code = device_code[4:-1]

        return device_code

    def skip_repeat(self, code):
        device_code = self.handle_device_code(code)
        equipment_qs = Equipment.search(code = device_code)
        if equipment_qs.count() > 0:
            self._error_msg = "该设备编码重复"
            return False
        else:
            equipment_in_qs = EquipmentIn.search(min_number__lte = device_code, \
                                                 max_number__gte = device_code)
            if equipment_in_qs.count() > 0:
                self._equipment_in = equipment_in_qs[0]
                product_model_qs = ProductModel.query().filter(name = self._equipment_in.product_model)
                if product_model_qs.count() > 0:
                    self._product_model = product_model_qs[0]
                else:
                    self._error_msg = "该设备型号不存在，请联系管理员添加"
                    return False
            else:
                self._error_msg = "该设备编码号段异常，不在入库号段内"
                return False

            equipment_out_qs = EquipmentOut.search(min_number__lte = device_code, \
                                                 max_number__gte = device_code)
            if equipment_out_qs.count() == 0:
                self._error_msg = "该设备编码号段异常，不在出库号段内"
                return False

        self._device_code = device_code

        return True

    def analysis_remark(self, remark):
            try:
                staff_name = re.findall(".*kf(.*)kf.*", remark)[0].strip()
                check_staff = self.convet_staff(staff_name)
                if not check_staff:
                    return False
            except Exception as e:
                self._error_msg = "缺少备注客服"
                return False
            try:
                mobile_code = re.findall(".*wx(.*)wx.*", remark)[0].strip()
                check__mobiledevices = self.convet_mobiledevices(mobile_code)
                if not check__mobiledevices:
                    return False
            except Exception as e:
                self._error_msg = "缺少备注手机编码"
                return False
            try:
                self._remark_pure = re.findall(".*bz(.*)bz.*", remark)[0].strip()
            except Exception as e:
                pass

            return True

    def convet_staff(self, staff_name):
        staff_alias_qs = StaffAlias.search(alias = staff_name)
        if staff_alias_qs.count() > 0:
            self._staff = staff_alias_qs[0].staff
        else:
            staff_qs = Staff.get_staff_byname(Q(name = staff_name) \
                        | Q(number = staff_name))

            if staff_qs.count() > 0:
                self._staff = staff_qs[0]
            else:
                self._error_msg = "备注客服不存在"
                return False

        return True

    def convet_mobiledevices(self, mobile_code):
        mobile_devices_qs = MobileDevices.query().filter(code = mobile_code)
        if mobile_devices_qs.count() > 0:
            self._mobiledevices = mobile_devices_qs[0]
            mobile_maintain_qs = MobileMaintain.search(devices = self._mobiledevices)
            if mobile_maintain_qs.count() > 0:
                self._server_staff = mobile_maintain_qs[0].staff
        else:
            self._error_msg = "备注手机编码系统不存在"
            return False

        return True

    def convet_customer(self, name, province, city, area, address, buy_phone, buy_nick):
        customer = None
        phone = buy_phone.strip()[:11]
        customer_qs = Customer.search(phone = phone)
        if customer_qs.count() > 0:
            customer = customer_qs[0]
        else:
            city_info = "{p}{c}{a}".format(p = province, c = city, a = area)
            customer = Customer.create(name = name, city = city_info, address = address, phone = phone, \
                                       nick = buy_nick, mobiledevices = self._mobiledevices, remark = buy_phone)
        return customer

    def convet_goods(self, name, buy_number, buy_money):
        goods = None
        goods_qs = Goods.query().filter(name = name)
        if goods_qs.count() > 0:
            goods = goods_qs[0]
        else:
            try:
                price = int(buy_money / buy_number)
            except Exception as e:
                price = 0

            goods = Goods.create(name = name, alias = name, price = price, shop = self._shop, product_model = self._product_model)

        return goods

    def convet_order(self, order_sn, buy_money, buy_number, pay_time, buy_name, province, city, \
                     area, address, buy_phone, customer):
        order = None
        order_qs = Order.search(order_sn = order_sn)
        if order_qs.count() > 0:
            order = order_qs[0]
        else:
            city_info = "{p}{c}{a}".format(p = province, c = city, a = area)
            order = Order.create(order_sn = order_sn, total_price = buy_money, total_quantity = buy_number, \
                                 pay_time = pay_time, status = StatusTypes.SENDED, consignee = buy_name, \
                                 city = city_info, address = address, phone = buy_phone, customer = customer, \
                                 shop = self._shop, remark = self._remark_pure)
        return order

    def convet_sale_chance(self, staff, customer, goods, order):
        sale_chance = None
        sale_chance_qs = SaleChance.search(create_time__lt = order.pay_time, end_time__gte = order.pay_time, \
                                           customer = customer, staff = staff, shop = self._shop, goods = goods)
        if sale_chance_qs.count() > 0:
            sale_chance = sale_chance_qs[0]
            order_list = json.loads(sale_chance.order_ids)
            order_list.append(order.id)
            order_ids = json.dumps(order_list)
            sale_chance.update(order_count = sale_chance.order_count + 1, order_ids = order_ids)
        else:
            create_time = order.pay_time - datetime.timedelta(days = 10)
            end_time = order.pay_time + datetime.timedelta(days = 5)
            sale_chance = SaleChance.create(staff = staff, customer = customer, shop = self._shop, goods = goods, \
                                            order_count = 1, order_ids = [order.id], end_time = end_time, \
                                             create_time = create_time)
        return sale_chance

    def convet_measure_staff(self, staff, pay_time):
        buy_data = datetime.datetime(pay_time.year, pay_time.month, pay_time.day)
        measure_staff_qs = MeasureStaff.search(staff = staff, report_date = buy_data)
        if measure_staff_qs.count() == 0:
            MeasureStaff.create(staff = staff, report_date = buy_data)
