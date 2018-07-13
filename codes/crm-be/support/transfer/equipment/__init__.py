# coding=UTF-8
import json
import datetime
import time

from support.transfer.base import BaseTransfer
from model.store.model_customer import Customer
from model.store.model_equipment import Equipment
from model.store.model_mobilephone import MobileDevices, MobileMaintain
from model.store.model_shop import Shop, Goods
from model.store.model_equipment_in import EquipmentIn
from model.store.model_product import ProductModel
from model.store.model_order import Order, OrderItem
from model.store.model_customer_chance import SaleChance
from model.store.model_order_event import StaffOrderEvent
from model.store.model_logistics import Logistics, LogisticsItem
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import Service, ServiceItem
from model.store.model_record_error import RecordError


class EquipmentTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select a.create_date,a.modify_date,a.nickname,a.buy_address,a.buy_date,a.buy_mobile,\
            a.customer_name,a.product_name,a.terminal_code,a.wechat,a.wechatname,a.wechat_index,a.shopname,\
            a.remarks,a.document_number,a.buy_num,a.buy_name,a.wl_number,a.wl_company,a.sn_color,\
            a.order_id,a.buy_price,a.buyinfo_color,b.name as staff_name,c.name as shop_name from ct_channel_user a \
            left join ct_admin b ON a.customer=b.id left join ct_sale_channel c ON a.sale_channel_id=c.id where a.is_buyinfo=1 and a.is_dsinfo is null"

    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            try:
                self.generate_date(data_list)
            except Exception as e:
                RecordError.create(remark = e)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束==================")


    def generate_date(self, data_list):
        for dic_data in data_list:
            equipment = self.skip_equipment(dic_data["terminal_code"])

            # 获取入库表
            equipment_in = self.get_equipment_in(dic_data["terminal_code"])
            self._modify_date = dic_data["modify_date"]
            self._create_date = dic_data["create_date"]

            # 获取员工
            staff = self.get_staff_byname(dic_data["staff_name"])
            # 获取手机设备
            mobile_devices = self.get_mobile_devices(dic_data["wechat_index"])
            # 获取店铺
            shop = self.get_shop(dic_data["shop_name"], dic_data["shopname"], dic_data["terminal_code"])
            # 获取客户
            customer = self.get_customer(dic_data["nickname"], dic_data["buy_address"], \
                                         dic_data["buy_mobile"], dic_data["buy_name"], mobile_devices, dic_data["terminal_code"])
            # 获取商品
            goods, product_model = self.get_goods(equipment_in, dic_data["product_name"], dic_data["buy_num"], \
                                   dic_data["buy_price"], shop, dic_data["terminal_code"])
            # 获取订单
            order = self.get_order(dic_data["buy_address"], dic_data["buy_date"], dic_data["buy_mobile"], \
                                   dic_data["remarks"], dic_data["buy_num"], dic_data["buy_name"], \
                                   dic_data["order_id"], dic_data["buy_price"], customer, shop, dic_data["document_number"], \
                                   dic_data["terminal_code"])
            # 获取订单详情
            order_item = OrderItem.create(order = order, goods = goods, name = goods.name, \
                                      alias = goods.name, price = goods.price, \
                                      quantity = order.total_quantity, update_time = dic_data["modify_date"], \
                                      create_time = dic_data["create_date"])
            # 获取销售机会
            sale_chance = self.get_sale_chance(staff, customer, shop, goods, order.pay_time, order)
            # 获取订单事件
            if staff is not None:
                staff_order_event = StaffOrderEvent.create(staff = staff, order = order, remark = dic_data["remarks"], \
                                                           update_time = dic_data["modify_date"], create_time = dic_data["create_date"])
            # 获取物流
            logistics = Logistics.create(order = order, customer = customer, company = dic_data["wl_company"] if dic_data["wl_company"] else "顺丰速运", \
                                         number = dic_data["wl_number"] if dic_data["wl_number"] else "BQ001", total_quantity = order.total_quantity, \
                                         update_time = dic_data["modify_date"], create_time = dic_data["create_date"])
            # 获取物流详情
            logistics_item = LogisticsItem.create(customer = customer, logistics = logistics, order_item = order_item, \
                                                  quantity = order.total_quantity, \
                                                  update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

                # 判断是否存在该设备
            if equipment is None:

                # 获取设备信息
                equipment = Equipment.create(customer = customer, logistics_item = logistics_item, order = order, \
                                             code = dic_data["terminal_code"], product_model = product_model, \
                                             product = product_model.product if product_model else None, \
                                             update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

                # 获取售后服务人
                server_staff = None
                if mobile_devices is not None:
                    server_staff = self.get_server_staff(mobile_devices)

                # 获取售后服务单
                service = Service.create(seller = staff, server = server_staff, customer = customer, order = order, \
                                         end_time = datetime.datetime.now() + datetime.timedelta(days = 5), \
                                         update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

                # 获取售后服务单详情
                service_item = ServiceItem.create(customer = customer, service = service, equipment = equipment, \
                                                  order = order, buyinfo_status = dic_data["buyinfo_color"], \
                                                  dsinfo_status = "red", \
                                                  sn_status = dic_data["sn_color"], \
                                                  rebate_status = "red", \
                                                  update_time = dic_data["modify_date"], create_time = dic_data["create_date"])
            else:
                # 获取售后服务单详情
                service_item_qs = ServiceItem.search(equipment = equipment)

                # 获取设备信息
                equipment.update(customer = customer, logistics_item = logistics_item, order = order, \
                                             product_model = product_model, \
                                             product = product_model.product if product_model else None)

                # 获取售后服务人
                server_staff = None
                if mobile_devices is not None:
                    server_staff = self.get_server_staff(mobile_devices)

                # 获取售后服务单
                service = Service.create(seller = staff, server = server_staff, customer = customer, order = order, \
                                         end_time = datetime.datetime.now() + datetime.timedelta(days = 5), \
                                         update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

                if service_item_qs.count() > 0:
                    service_item = service_item_qs[0]
                    service_item.update(customer = customer, service = service, \
                                       order = order, buyinfo_status = dic_data["buyinfo_color"])

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def skip_equipment(self, code):
        equipment = None
        if code:
            equipment_qs = Equipment.search(code = code)
            if equipment_qs.count() > 0:
                equipment = equipment_qs[0]

        return equipment


    def get_mobile_devices(self, code):
        mobile_devices = None
        if code:
            mobile_devices_qs = MobileDevices.search(code = code)
            if mobile_devices_qs.count() > 0:
                mobile_devices = mobile_devices_qs[0]
            else:
                mobile_devices = MobileDevices.create(code = code, update_time = self._modify_date, create_time = self._create_date)

        return mobile_devices


    def get_shop(self, shop_name, shopname, terminal_code):
        shop = None
        shop_name = shop_name
        if not shop_name:
            shop_name = shopname

        if shop_name:
            shop = Shop.get_shop_buyname(shop_name)
            if shop is None:
                shop = Shop.create(name = shop_name, update_time = self._modify_date, create_time = self._create_date)
        else:
            shop = Shop.get_shop_buyname("系统店铺")
            RecordError.create(remark = "缺少店铺:{c}".format(c = terminal_code))
        return shop


    def get_customer(self, nickname, buy_address, buy_mobile, buy_name, mobile_devices, terminal_code):
        customer = None
        if buy_name and buy_mobile:
            phone = buy_mobile.strip()[:11]
            customer_qs = Customer.search(phone = phone)
            if customer_qs.count() > 0:
                customer = customer_qs[0]
            else:
                customer = Customer.create(name = buy_name, address = buy_address, phone = phone, \
                                           nick = nickname, mobiledevices = mobile_devices, remark = buy_mobile, \
                                           update_time = self._modify_date, create_time = self._create_date)
        else:
            customer = Customer.search(name = "系统客户")[0]
            RecordError.create(remark = "缺少客户:{c}".format(c = terminal_code))
        return customer


    def get_equipment_in(self, device_code):
        equipment_in = None
        equipment_in_qs = EquipmentIn.search(min_number__lte = device_code, \
                                                 max_number__gte = device_code)
        if equipment_in_qs.count() > 0:
            equipment_in = equipment_in_qs[0]

        return equipment_in


    def get_goods(self, equipment_in, product_name, buy_num, buy_price, shop, terminal_code):
        goods = None
        product_model = None
        if equipment_in is not None:
            product_model_qs = ProductModel.query().filter(name = equipment_in.product_model)
            if product_model_qs.count() > 0:
                product_model = product_model_qs[0]

        if product_name:
            goods_qs = Goods.query().filter(name = product_name)
            if goods_qs.count() > 0:
                goods = goods_qs[0]
            else:
                try:
                    price = int(buy_price / buy_num * 100)
                except Exception as e:
                    price = 0
                goods = Goods.create(name = product_name, alias = product_name, price = price, \
                                     shop = shop, product_model = product_model, \
                                     update_time = self._modify_date, create_time = self._create_date)
        else:
            goods = Goods.query().filter(name = "系统商品")[0]
            RecordError.create(remark = "缺少商品:{c}".format(c = terminal_code))

        return goods, product_model


    def get_order(self, buy_address, buy_date, buy_mobile, remarks, buy_num, buy_name, order_id, buy_price, \
                  customer, shop, document_number, terminal_code):
        order = None
        order_sn = order_id
        if not order_id:
            if document_number:
                order_sn = document_number

        if order_sn:
            order_qs = Order.search(order_sn = order_sn)
            if order_qs.count() > 0:
                order = order_qs[0]
            else:
                try:
                    total_price = int(buy_price * 100)
                except Exception as e:
                    total_price = 0
                if not buy_num:
                    buy_num = 1
                order = Order.create(order_sn = order_sn, total_price = total_price, total_quantity = buy_num, \
                                     pay_time = buy_date if buy_date else self._create_date, status = "sended", consignee = buy_name, \
                                     address = buy_address, phone = buy_mobile, customer = customer, \
                                     shop = shop, remark = remarks, update_time = self._modify_date, create_time = self._create_date)
        else:
            order_sn = "other{t}".format(t = int(time.time()))  # 有问题
            try:
                total_price = int(buy_price * 100)
            except Exception as e:
                total_price = 0
            if not buy_num:
                buy_num = 1
            order = Order.create(order_sn = order_sn, total_price = total_price, total_quantity = buy_num, \
                                 pay_time = buy_date if buy_date else self._create_date, status = "sended", \
                                 consignee = buy_name if buy_name else customer.name, \
                                 address = buy_address if buy_address else customer.address, \
                                 phone = buy_mobile if buy_mobile else customer.phone, customer = customer, \
                                 shop = shop, remark = remarks, update_time = self._modify_date, create_time = self._create_date)

            RecordError.create(remark = "缺少订单:{c}".format(c = terminal_code))

        return order


    def get_sale_chance(self, staff, customer, shop, goods, buy_date, order):
        sale_chance = None
        sale_chance_qs = SaleChance.search(create_time__lt = buy_date, end_time__gte = buy_date, \
                                           customer = customer, shop = shop, goods = goods)
        if sale_chance_qs.count() > 0:
            sale_chance = sale_chance_qs[0]
            order_list = json.loads(sale_chance.order_ids)
            order_list.append(order.id)
            order_ids = json.dumps(order_list)
            sale_chance.update(order_count = sale_chance.order_count + 1, order_ids = order_ids)
        else:
            create_time = buy_date - datetime.timedelta(days = 10)
            end_time = buy_date + datetime.timedelta(days = 5)
            sale_chance = SaleChance.create(staff = staff, customer = customer, shop = shop, goods = goods, \
                                            order_count = 1, order_ids = [order.id], end_time = end_time, \
                                             create_time = create_time)
        return sale_chance

    def get_server_staff(self, mobile_devices):
        server_staff = None
        mobile_maintain_qs = MobileMaintain.search(devices = mobile_devices)
        if mobile_maintain_qs.count() > 0:
            server_staff = mobile_maintain_qs[0].staff

        return server_staff

    def get_rebate_status(self, sn_color):
        rebate_status = sn_color
        if sn_color == "green":
            rebate_status = "tgreen"
        elif sn_color == "green1":
            rebate_status = "green"

        return rebate_status
