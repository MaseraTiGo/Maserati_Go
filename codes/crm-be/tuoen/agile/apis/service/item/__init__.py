# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField, DateField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.service.manager import ServiceServer, ServiceItemServer
from tuoen.abs.service.order.manager import OrderServer
from tuoen.abs.service.equipment.manager import EquipmentRegisterServer
from tuoen.abs.service.authority import UserRightServer

class Search(StaffAuthorizedApi):
    """售后服务单产品列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        "equipment_code":CharField(desc = "设备编码", is_required = False),
        "seller_staff_id":IntField(desc = "售前客服id", is_required = False),
        "server_staff_id":IntField(desc = "售后客服id", is_required = False),
        "shop_id":CharField(desc = "店铺id", is_required = False),
        "buy_date_start":DateField(desc = "购买起始时间", is_required = False),
        "buy_date_end":DateField(desc = "购买结束时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '售后服务单产品列表', fmt = DictField(desc = "售后服务单产品列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "购买人"),
        'phone': CharField(desc = "购买人电话"),
        'code': CharField(desc = "SN码"),
        'pre_id': IntField(desc = "售前客服id"),
        'pre_name': CharField(desc = "售前客服"),
        'after_id': IntField(desc = "售后客服id"),
        'after_name': CharField(desc = "售后客服"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'buy_time': DatetimeField(desc = "购买时间"),
        'create_time': DatetimeField(desc = "录入时间"),
        'buyinfo_status': CharField(desc = "购买信息状态"),
        'dsinfo_status': CharField(desc = "电刷信息状态"),
        'rebate_status': CharField(desc = "激活信息状态"),
        'sn_status': CharField(desc = "设备码出入库状态"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "售后服务单产品列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        request.search_info.update({"service__seller_id__in": user_pro._staff_id_list})

        page_list = ServiceItemServer.search(request.current_page, **request.search_info)

        # 挂载售前售后客服
        ServiceServer.hung_staff_forservice(page_list.data)
        # 挂载店铺
        OrderServer.hung_shop_forservice(page_list.data)


        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': service_item.id,
            'name': service_item.customer.name if service_item.customer else "",
            'phone': service_item.customer.phone if service_item.customer else "",
            'code': service_item.equipment.code,
            'pre_id': service_item.pre_staff.id if service_item.pre_staff else 0,
            'pre_name': service_item.pre_staff.name if service_item.pre_staff else "",
            'after_id': service_item.after_staff.id if service_item.after_staff else 0,
            'after_name': service_item.after_staff.name if service_item.after_staff else "",
            'shop_id': service_item.shop.id if service_item.shop else 0,
            'shop_name': service_item.shop.name if service_item.shop else "",
            'buy_time': service_item.order.pay_time if service_item.order else "",
            'create_time': service_item.create_time,
            'buyinfo_status': service_item.buyinfo_status,
            'dsinfo_status': service_item.dsinfo_status,
            'rebate_status': service_item.rebate_status,
            'sn_status': service_item.sn_status,
        } for service_item in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Get(StaffAuthorizedApi):
    """售后服务单产品信息"""
    request = with_metaclass(RequestFieldSet)
    request.service_item_id = RequestField(IntField, desc = "售后服务单id")

    response = with_metaclass(ResponseFieldSet)
    response.service_item_info = ResponseField(DictField, desc = '售后服务单产品信息', conf = {
        'customer_id': IntField(desc = "客户id"),
        'customer_name': CharField(desc = "客户姓名"),
        'customer_phone': CharField(desc = "客户联系方式"),
        'device_code': CharField(desc = "设备编码"),
        'buy_date': DatetimeField(desc = "购买时间"),
        'wechat': CharField(desc = "微信号"),
        'nick': CharField(desc = "微信昵称"),
        'remark': CharField(desc = "备注"),

        'register_id': IntField(desc = "id"),
        'register_phone': CharField(desc = "注册手机号"),
        'register_name': CharField(desc = "注册姓名"),
    })

    @classmethod
    def get_desc(cls):
        return "售后服务单产品信息接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        service_item = ServiceItemServer.get(request.service_item_id)
        service = None
        if service_item.service:
            service = ServiceServer.get(service_item.service.id)
        equipment_register = EquipmentRegisterServer.get_register_byequipment(service_item.equipment)
        return service_item, service, equipment_register

    def fill(self, response, service_item, service, equipment_register):
        response.service_item_info = {
            'customer_id': service_item.customer.id if service_item.customer else 0,
            'customer_name': service_item.customer.name if service_item.customer else "",
            'customer_phone': service_item.customer.phone if service_item.customer else "",
            'device_code': service_item.equipment.code,
            'buy_date': service.order.pay_time if service_item.order else "",
            'wechat': service_item.customer.wechat if service_item.customer else "",
            'nick': service_item.customer.nick if service_item.customer else "",
            'remark': service.order.remark if service_item.order else "",

            'register_id': equipment_register.id if equipment_register else 0,
            'register_phone': equipment_register.phone if equipment_register else "",
            'register_name': equipment_register.name if equipment_register else "",
        }
        return response
