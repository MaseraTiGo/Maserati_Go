# coding=UTF-8

from tuoen.abs.middleware.rule.base import BaseRule
from tuoen.abs.middleware.rule.entity import RuleEntity


class Action(object):
    QUERY = ("query", "查询")
    ADD = ("add", "添加")
    EDIT = ("edit", "编辑")
    DELETE = ("delete", "删除")
    UPLOAD = ("upload", "上传")
    CONVERT = ("convert", "转化")
    ALLOT = ("allot", "分配")
    ADDEVENT = ("addevent", "添加事件")

class Permise(BaseRule):
    DEFAULT = RuleEntity("permise", "权限管理")

    DEFAULT_DEPARTMENT = RuleEntity("department", "部门管理")
    DEFAULT_DEPARTMENT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_DEPARTMENT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_DEPARTMENT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_DEPARTMENT_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_ROLE = RuleEntity("role", "角色管理")
    DEFAULT_ROLE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROLE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROLE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ROLE_DEL = RuleEntity(*Action.DELETE)


class Staff(BaseRule):
    DEFAULT = RuleEntity("staff", "员工管理")

    DEFAULT_STAFF = RuleEntity("staff", "员工列表")
    DEFAULT_STAFF_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STAFF_ADD = RuleEntity(*Action.ADD)
    DEFAULT_STAFF_EDIT = RuleEntity(*Action.EDIT)

    DEFAULT_STAFFALIAS = RuleEntity("staffalias", "别名管理")
    DEFAULT_STAFFALIAS_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STAFFALIAS_ADD = RuleEntity(*Action.ADD)
    DEFAULT_STAFFALIAS_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_STAFFALIAS_DEL = RuleEntity(*Action.DELETE)

class Order(BaseRule):
    DEFAULT = RuleEntity("order", "订单管理")

    DEFAULT_ORDER = RuleEntity("order", "订单列表")
    DEFAULT_ORDER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ORDER_EDIT = RuleEntity(*Action.EDIT)

class Mobile(BaseRule):
    DEFAULT = RuleEntity("mobile", "手机管理")

    DEFAULT_MOBILEDEVICES = RuleEntity("mobiledevices", "手机设备")
    DEFAULT_MOBILEDEVICES_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEDEVICES_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILEDEVICES_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEDEVICES_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MOBILEPHONE = RuleEntity("mobilephone", "号码管理")
    DEFAULT_MOBILEPHONE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEPHONE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILEPHONE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEPHONE_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MOBILETAINTAIN = RuleEntity("mobilemaintain", "设备维护")
    DEFAULT_MOBILETAINTAIN_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILETAINTAIN_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILETAINTAIN_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILETAINTAIN_DEL = RuleEntity(*Action.DELETE)

class Customer(BaseRule):
    DEFAULT = RuleEntity("customer", "客户管理")

    DEFAULT_CUSTOMER = RuleEntity("customer", "客户列表")
    DEFAULT_CUSTOMER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CUSTOMER_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_CUSTOMER_ALLOT = RuleEntity(*Action.ALLOT)

class SaleChance(BaseRule):
    DEFAULT = RuleEntity("salechance", "销售机会")

    DEFAULT_SALECHANCE = RuleEntity("salechance", "机会列表")
    DEFAULT_SALECHANCE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SALECHANCE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_SALECHANCE_ADDTRACK = RuleEntity(*Action.ADDEVENT)

class ServiceItem(BaseRule):
    DEFAULT = RuleEntity("serviceitem", "设备管理")

    DEFAULT_SERVICEITEM = RuleEntity("serviceitem", "设备管理")
    DEFAULT_SERVICEITEM_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SERVICEITEM_EDIT = RuleEntity(*Action.EDIT)

class Shop(BaseRule):
    DEFAULT = RuleEntity("shop", "店铺管理")

    DEFAULT_CHANNEL = RuleEntity("channel", "店铺渠道管理")
    DEFAULT_CHANNEL_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CHANNEL_ADD = RuleEntity(*Action.ADD)
    DEFAULT_CHANNEL_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_CHANNEL_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_SHOP = RuleEntity("shop", "店铺管理")
    DEFAULT_SHOP_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SHOP_ADD = RuleEntity(*Action.ADD)
    DEFAULT_SHOP_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_SHOP_DEL = RuleEntity(*Action.DELETE)

class Measure(BaseRule):
    DEFAULT = RuleEntity("measure", "绩效管理")

    DEFAULT_MEASURESHOP = RuleEntity("measureshop", "店铺绩效")
    DEFAULT_MEASURESHOP_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MEASURESHOP_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MEASURESHOP_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MEASURESHOP_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MEASURESTAFF = RuleEntity("measurestaff", "员工绩效")
    DEFAULT_MEASURESTAFF_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MEASURESTAFF_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MEASURESTAFF_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MEASURESTAFF_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_STATISTICS = RuleEntity("statistics", "员工绩效统计")
    DEFAULT_STATISTICS_QUERY = RuleEntity(*Action.QUERY)

class DataImport(BaseRule):
    DEFAULT = RuleEntity("dataimport", "数据导入")

    DEFAULT_BUYINFO = RuleEntity("buyinfo", "购买信息")
    DEFAULT_BUYINFO_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_BUYINFO_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_BUYINFO_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_BUYINFO_CONVERT = RuleEntity(*Action.CONVERT)

    DEFAULT_EQUIPMENTIN = RuleEntity("equipmentin", "设备入库")
    DEFAULT_EQUIPMENTIN_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTIN_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_EQUIPMENTIN_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_EQUIPMENTIN_CONVERT = RuleEntity(*Action.CONVERT)
    
    DEFAULT_EQUIPMENTOUT = RuleEntity("equipmentout", "设备出库")
    DEFAULT_EQUIPMENTOUT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTOUT_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_EQUIPMENTOUT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_EQUIPMENTOUT_CONVERT = RuleEntity(*Action.CONVERT)
    
    DEFAULT_REGISTER = RuleEntity("register", "客户注册")
    DEFAULT_REGISTER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_REGISTER_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_REGISTER_CONVERT = RuleEntity(*Action.CONVERT)
    
    DEFAULT_REBATE = RuleEntity("rebate", "客户返利")
    DEFAULT_REBATE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_REBATE_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_REBATE_CONVERT = RuleEntity(*Action.CONVERT)

    DEFAULT_TRANSACTION = RuleEntity("transaction", "交易流水")
    DEFAULT_TRANSACTION_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_TRANSACTION_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_TRANSACTION_CONVERT = RuleEntity(*Action.CONVERT)

    DEFAULT_STAFFIMPORT = RuleEntity("staffimport", "员工导入")
    DEFAULT_STAFFIMPORT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STAFFIMPORT_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_STAFFIMPORT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_STAFFIMPORT_CONVERT = RuleEntity(*Action.CONVERT)

    DEFAULT_MOBILEDEVICES = RuleEntity("mobiledevices", "手机设备")
    DEFAULT_MOBILEDEVICES_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEDEVICES_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_MOBILEDEVICES_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEDEVICES_CONVERT = RuleEntity(*Action.CONVERT)

    DEFAULT_MOBILEPHONE = RuleEntity("mobilephone", "手机号码")
    DEFAULT_MOBILEPHONE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEPHONE_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_MOBILEPHONE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEPHONE_CONVERT = RuleEntity(*Action.CONVERT)

class Product(BaseRule):
    DEFAULT = RuleEntity("product", "产品管理")
    
    DEFAULT_PRODUCT = RuleEntity("product", "产品列表")
    DEFAULT_PRODUCT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PRODUCT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_PRODUCT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_PRODUCT_DEL = RuleEntity(*Action.DELETE)
    
    DEFAULT_PRODUCTMODEL = RuleEntity("productmodel", "型号管理")
    DEFAULT_PRODUCTMODEL_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PRODUCTMODEL_ADD = RuleEntity(*Action.ADD)
    DEFAULT_PRODUCTMODEL_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_PRODUCTMODEL_DEL = RuleEntity(*Action.DELETE)
    
 

permise_rules = Permise()
staff_rules = Staff()
order_rules = Order()
mobile_rules = Mobile()
customer_rules = Customer()
sale_chance_rules = SaleChance()
service_item_rules = ServiceItem()
shop_rules = Shop()
measure_rules = Measure()
data_import_rules = DataImport()
product_rules = Product()