# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.order.manager import StaffOrderEventServer, OrderServer, OrderItemServer
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.logistics.manager import LogisticsServer
from tuoen.abs.service.service.manager import ServiceServer
from tuoen.abs.service.equipment.manager import EquipmentServer
from tuoen.abs.service.authority import UserRightServer


class Search(StaffAuthorizedApi):
    """订单列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'order_sn': CharField(desc = "订单号", is_required = False),
        'status': CharField(desc = "订单状态(unpaid:未支付,submit:已下单,payed:已支付,sended:已发货,finished:已完成)", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '订单列表', fmt = DictField(desc = "订单列表", conf = {
        'id': IntField(desc = "id"),
        'order_sn': CharField(desc = "订单编号"),
        'shop_name': CharField(desc = "店铺名称"),
        'consignee': CharField(desc = "收货人"),
        'nick_name': CharField(desc = "昵称"),
        'status': CharField(desc = "订单状态"),
        'create_time': DatetimeField(desc = "添加时间"),
        'order_items': ListField(desc = '订单详情', fmt = DictField(desc = "订单详情", conf = {
           'name': CharField(desc = "商品名称"),
           'thumbnail': CharField(desc = "商品缩略图"),
           'rate':CharField(desc = "商品费率"),
           'quantity':IntField(desc = "商品数量"),
           'type':CharField(desc = "商品分类"),
           'brand_name':CharField(desc = "商品型号"),
        })),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "订单列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        user_pro = UserRightServer(staff)
        request.search_info['cur_user'] = user_pro
        if staff.is_admin == 1:
            page_list = OrderServer.search(request.current_page, **request.search_info)
        else:

            staff_list = StaffPermiseServer.get_all_children_staff(staff)
            staff_list.append(staff)            
            page_list = ServiceServer.search(request.current_page, seller__in = staff_list, cur_user = user_pro)
            order_list = OrderServer.get_order_byservice(page_list.data)
            page_list.data = order_list

        page_list.data = OrderItemServer.hung_item_fororders(page_list.data)

        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': order.id,
            'order_sn': order.order_sn,
            'shop_name': order.shop.name,
            'consignee': order.consignee,
            'nick_name': order.customer.nick,
            'status': order.status,
            'create_time': order.create_time,
            'order_items':[{
                         'name':order_item.name,
                         'thumbnail':order_item.thumbnail,
                         'rate':order_item.rate,
                         'quantity':order_item.quantity,
                         'type':order_item.type,
                         'brand_name':order_item.goods.product_model.name if order_item.goods and order_item.goods.product_model else "",
                         } for order_item in order.items]
        } for order in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取订单详情"""
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = '订单id')

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(DictField, desc = "订单详情", conf = {
        'id': IntField(desc = "id"),
        'order_sn': CharField(desc = "订单编号"),
        'consignee': CharField(desc = "收货人"),
        'nick_name': CharField(desc = "昵称"),
        'phone': CharField(desc = "收货人电话"),
        'city': CharField(desc = "城市"),
        'address': CharField(desc = "详细地址"),
        'messages': CharField(desc = "买家留言"),
        'paytype': CharField(desc = "支付类型"),
        'pay_time': CharField(desc = "付款时间"),
        'transaction_id': CharField(desc = "第三方支付id"),
        'total_price': IntField(desc = "订单金额"),
        'channel_name': CharField(desc = "渠道名称"),
        'shop_name': CharField(desc = "店铺名称"),
        'create_time': CharField(desc = "创建时间"),
        'remark': CharField(desc = "卖家备注"),
        'order_items': ListField(desc = '订单详情', fmt = DictField(desc = "订单详情", conf = {
           'name': CharField(desc = "商品名称"),
           'thumbnail': CharField(desc = "商品缩略图"),
           'rate':CharField(desc = "商品费率"),
           'price':IntField(desc = "商品单价"),
           'type':CharField(desc = "商品类型"),
           'brand_name':CharField(desc = "商品型号"),
           'quantity':IntField(desc = "商品数量"),
        })),
        'logistics': ListField(desc = '物流列表', fmt = DictField(desc = "物流列表", conf = {
           'company': CharField(desc = "物流公司"),
           'number': CharField(desc = "物流单号"),
           'total_quantity':IntField(desc = "发货数量"),
           'create_time':DatetimeField(desc = "发货时间"),
           'logistics_items': ListField(desc = "订单详情", fmt = DictField(desc = "订单详情", conf = {
               'name': CharField(desc = "商品名称"),
               'thumbnail': CharField(desc = "商品缩略图"),
               'quantity':IntField(desc = "商品数量"),
               'equipment_codes':ListField(desc = "设备编码列表", fmt = DictField(desc = "设备编码列表", conf = {
                    'code': CharField(desc = "设备编码"),
                })),
            })),
        })),
    })

    @classmethod
    def get_desc(cls):
        return "订单详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        OrderItemServer.hung_item_fororder(order)
        LogisticsServer.hung_item_fororser(order)

        EquipmentServer.hung_code_bylogistics(order.logistics)

        return order

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'order_sn': order.order_sn,
            'consignee': order.consignee,
            'nick_name': order.customer.nick,
            'phone': order.phone,
            'city': order.city,
            'address': order.address,
            'messages': order.messages,
            'paytype': order.paytype,
            'pay_time': order.pay_time,
            'transaction_id': order.transaction_id,
            'total_price': order.total_price,
            'channel_name': order.shop.channel.name if order.shop.channel else "",
            'shop_name': order.shop.name,
            'create_time': order.create_time,
            'remark': order.remark,
            'order_items':[{
                         'name':orderitem.name,
                         'thumbnail':orderitem.thumbnail,
                         'rate':orderitem.rate,
                         'price':orderitem.price,
                         'type':orderitem.type,
                         'brand_name':orderitem.goods.product_model.name if orderitem.goods and orderitem.goods.product_model else "",
                         'quantity':orderitem.quantity,
                         } for orderitem in order.items],
            'logistics':[{
                         'company': logistics.company,
                         'number': logistics.number,
                         'total_quantity':logistics.total_quantity,
                         'create_time':logistics.create_time,
                         'logistics_items':[{
                             'name': logisticsitem.order_item.name,
                             'thumbnail': logisticsitem.order_item.thumbnail,
                             'quantity':logisticsitem.quantity,
                             'equipment_codes':[{
                                 'code': equipment.code,
                                 } for equipment in logisticsitem.equipment_list]
                             } for logisticsitem in logistics.items]
                         } for logistics in order.logistics]
        }
        return response
