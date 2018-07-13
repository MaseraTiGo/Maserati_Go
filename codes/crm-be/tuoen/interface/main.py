# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import json
import itertools

from django.http.response import HttpResponse
from django.shortcuts import render_to_response

import tuoen.sys.utils.common.signature as signature
from tuoen.sys.core.api.doc import TextApiDoc
from tuoen.sys.core.exception.api_error import api_errors
from tuoen.sys.core.exception.pro_error import pro_errors
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.exception.system_error import SysError

from tuoen.agile.protocol.base import DjangoProtocol
from tuoen.agile.server.app.base import user_service
from tuoen.agile.server.file.base import file_service

from tuoen.abs.middleware.rule import rule_register


protocol = DjangoProtocol()
protocol.add(user_service)
protocol.add(file_service)


def router(request):
    result = protocol.run(request)
    resp = HttpResponse(json.dumps(result))
    resp['Access-Control-Allow-Origin'] = '*'  # 处理跨域请求
    return resp


def api_doc(request):
    api_signature_doc = signature.__doc__
    services = protocol.get_services()
    for service in services:
        apis = service.get_apis()
        service.api_docs = [TextApiDoc(api) for api in apis]

    error_list = []
    error_list.append(SysError)
    error_list.extend(pro_errors.get_errors())
    error_list.extend(api_errors.get_errors())
    error_list.append(BusinessError)
    error_list = [(err.get_flag(), err.get_code(), err.get_desc()) for err in error_list]

    return render_to_response('api_index.html', {
        'api_signature_doc': api_signature_doc,
        'services': services,
        'error_list': error_list,
    })

def premise_doc(request):
    rule_roots = rule_register.get_roots()
    return render_to_response('premise_index.html', {
        'root_list': rule_roots
    })
