# coding=UTF-8

from tuoen.sys.core.field.adapter import AdapterField, AdapterFieldSet


class ResponseField(AdapterField):

    def __init__(self, field_cls, *args, **kwargs):
        super(ResponseField, self).__init__(field_cls, *args, **kwargs)

    def execute(self, value):
        return self.get_field().format(value)


class ResponseFieldSet(AdapterFieldSet):

    _field_cls = ResponseField
