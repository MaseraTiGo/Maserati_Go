# coding=UTF-8


from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_register_middleware


class Upload(StaffAuthorizedApi):
    """客户注册数据导入接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "客户注册数据导入接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            print(file_name)
            # print(file_name, file_io.read())
            data_list, errors = import_register_middleware.import_register(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """客户注册数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "客户编码", is_required = False),
        'device_code': CharField(desc = "设备编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户注册数据列表', fmt = DictField(desc = "客户注册数据列表", conf = {
        'id': IntField(desc = "id"),
        'agent_name': CharField(desc = "代理商名称"),
        'code': CharField(desc = "客户编码"),
        'phone': CharField(desc = "注册手机号"),
        'name': CharField(desc = "客户姓名"),
        'register_time': DatetimeField(desc = "注册时间"),
        'bind_time': DatetimeField(desc = "绑定时间"),
        'device_code': CharField(desc = "设备编码"),
        'status': CharField(desc = "执行状态"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户注册数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_register_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': register.id,
            'agent_name': register.agent_name,
            'code': register.code,
            'phone': register.phone,
            'name': register.name,
            'register_time': register.register_time,
            'bind_time': register.bind_time,
            'device_code': register.device_code,
            'status': register.status,
            'create_time': register.create_time,
            'error_text': register.error_text
        } for register in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Convert(StaffAuthorizedApi):
    """客户注册数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户注册数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_register_middleware.exec_register(**request.search_info)

    def fill(self, response):
        return response
