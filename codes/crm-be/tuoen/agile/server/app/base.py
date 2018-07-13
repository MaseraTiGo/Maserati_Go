# coding=UTF-8

from tuoen.sys.core.service.base import BaseAPIService
from tuoen.abs.middleware.rule import rule_register, permise_rules, staff_rules, \
                                    order_rules, mobile_rules, customer_rules, sale_chance_rules, \
                                    shop_rules, service_item_rules, measure_rules, data_import_rules, \
                                    product_rules

from tuoen.agile.apis import test


class UserService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "用户服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录用户提供服务"

    @classmethod
    def get_flag(cls):
        return "user"


user_service = UserService()
from tuoen.agile.apis.account.staff import Login, Generate
user_service.add(Login, Generate)


from tuoen.agile.apis.account.staff.update import Password
user_service.add(Password)


from tuoen.agile.apis.user.staff import Add, Get, Update, Search, SearchAll, UpdateByAdmin, GetByadmin, Match, SearchAllFaker
user_service.add(Add, Get, Update, Search, SearchAll, UpdateByAdmin, GetByadmin, Match, SearchAllFaker)
rule_register.register_api(staff_rules.DEFAULT_STAFF_QUERY, Search)
rule_register.register_api(staff_rules.DEFAULT_STAFF_EDIT, GetByadmin, UpdateByAdmin)
rule_register.register_api(staff_rules.DEFAULT_STAFF_ADD, Add)


from tuoen.agile.apis.user.token import Renew
user_service.add(Renew)


from tuoen.agile.apis.journal import Search
user_service.add(Search)


from tuoen.agile.apis.permise.staff.role import Add, List, Update, Remove, Get
user_service.add(Add, List, Update, Remove, Get)
rule_register.register_api(permise_rules.DEFAULT_ROLE_QUERY, List)
rule_register.register_api(permise_rules.DEFAULT_ROLE_ADD, Add)
rule_register.register_api(permise_rules.DEFAULT_ROLE_EDIT, Get, Update)
rule_register.register_api(permise_rules.DEFAULT_ROLE_DEL, Remove)

from tuoen.agile.apis.permise.staff.rule import List
user_service.add(List)

from tuoen.agile.apis.permise.staff.department import Add, List, Update, Remove, Get
user_service.add(Add, List, Update, Remove, Get)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_QUERY, List)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_ADD, Add)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_EDIT, Get, Update)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_DEL, Remove)


from tuoen.agile.apis.mobile.devices import Add, Search, Searchall, Get, Update, Remove
user_service.add(Add, Search, Searchall, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_DEL, Remove)

from tuoen.agile.apis.mobile.phone import Add, Search, Get, Update, Remove
user_service.add(Add, Search, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_DEL, Remove)

from tuoen.agile.apis.mobile.maintain import Add, Search, Get, Update, Remove
user_service.add(Add, Search, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_DEL, Remove)

from tuoen.agile.apis.shop.channel import Add, Search, Get, Update, Remove, Match, SearchAll
user_service.add(Add, Search, Get, Update, Remove, Match, SearchAll)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_QUERY, Search)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_ADD, Add)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_EDIT, Get, Update)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_DEL, Remove)


from tuoen.agile.apis.shop import Add, Search, Get, Update, Remove, Match, SearchAll
user_service.add(Add, Search, Get, Update, Remove, Match, SearchAll)


rule_register.register_api(shop_rules.DEFAULT_SHOP_QUERY, Search)
rule_register.register_api(shop_rules.DEFAULT_SHOP_ADD, Add)
rule_register.register_api(shop_rules.DEFAULT_SHOP_EDIT, Get, Update)
rule_register.register_api(shop_rules.DEFAULT_SHOP_DEL, Remove)


from tuoen.agile.apis.shop.goods import Search, SearchAll, Match
user_service.add(Search, SearchAll, Match)


from tuoen.agile.apis.order import Search, Get
user_service.add(Search, Get)
rule_register.register_api(order_rules.DEFAULT_ORDER_QUERY, Search)
rule_register.register_api(order_rules.DEFAULT_ORDER_EDIT, Get)


from tuoen.agile.apis.measure.shop import Add, Search, Get, Update, Remove, Statistics
user_service.add(Add, Search, Get, Update, Remove, Statistics)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_QUERY, Search)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_ADD, Add)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_EDIT, Get, Update)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_DEL, Remove)

from tuoen.agile.apis.measure.staff import Add, Search, Get, Update, Remove, Statistics
user_service.add(Add, Search, Get, Update, Remove, Statistics)
rule_register.register_api(measure_rules.DEFAULT_MEASURESTAFF_QUERY, Search)
rule_register.register_api(measure_rules.DEFAULT_MEASURESTAFF_ADD, Add)
rule_register.register_api(measure_rules.DEFAULT_MEASURESTAFF_EDIT, Get, Update)
rule_register.register_api(measure_rules.DEFAULT_MEASURESTAFF_DEL, Remove)

from tuoen.agile.apis.measure import Statistics
user_service.add(Statistics)
rule_register.register_api(measure_rules.DEFAULT_STATISTICS_QUERY, Statistics)

from tuoen.agile.apis.service.item import Search, Get
user_service.add(Search, Get)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_QUERY, Search)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Get)

from tuoen.agile.apis.customer import Search, Get, Update
user_service.add(Search, Get, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_QUERY, Search)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_EDIT, Get, Update)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Update)

from tuoen.agile.apis.customer.sale.chance import Add, Search, Update
user_service.add(Add, Search, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_ALLOT, Add)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_QUERY, Search)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_EDIT, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_EDIT, Search)

from tuoen.agile.apis.event.track import Add, Search, SearchByTrack
user_service.add(Add, Search, SearchByTrack)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_QUERY, SearchByTrack)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_ADDTRACK, Add)

# data import
from tuoen.agile.apis.data.register import Upload, Search, Convert
user_service.add(Upload, Search, Convert)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.rebate import Upload, Search, Convert
user_service.add(Upload, Search, Convert)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.transaction import Upload, Search, Convert
user_service.add(Upload, Search, Convert)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.buyinfo import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.equipmentin import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.equipmentout import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.staff import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.mobiledevices import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_CONVERT, Convert)

# data import
from tuoen.agile.apis.data.mobilephone import Upload, Search, Convert, Update
user_service.add(Upload, Search, Convert, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_CONVERT, Convert)

from tuoen.agile.apis.equipment.register import Update
user_service.add(Update)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Update)

from tuoen.agile.apis.staffalias import Add, Search, Update, Remove
user_service.add(Add, Search, Update, Remove)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_QUERY, Search)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_EDIT, Update)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_ADD, Add)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_DEL, Remove)

from tuoen.agile.apis.product.product import Add, Search, Update, Remove
user_service.add(Add, Search, Update, Remove)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_QUERY, Search)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_EDIT, Update)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_ADD, Add)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_DEL, Remove)

from tuoen.agile.apis.product.productmodel import Add, Search, Update, Remove
user_service.add(Add, Search, Update, Remove)
rule_register.register_api(product_rules.DEFAULT_PRODUCTMODEL_QUERY, Search)
rule_register.register_api(product_rules.DEFAULT_PRODUCTMODEL_EDIT, Update)
rule_register.register_api(product_rules.DEFAULT_PRODUCTMODEL_ADD, Add)
rule_register.register_api(product_rules.DEFAULT_PRODUCTMODEL_DEL, Remove)
# demo
from tuoen.agile.apis.test.demo import Test, Filter
user_service.add(Test, Filter)

