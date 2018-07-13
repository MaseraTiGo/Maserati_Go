# coding=UTF-8

from tuoen.sys.core.api.base import BaseApi
from tuoen.sys.core.exception.debug_error import DebugError

from tuoen.abs.service.user.manager import UserServer, StaffServer
from tuoen.agile.apis.base import AuthorizedApi


class ServerAuthorizedApi(AuthorizedApi):

    def authorized(self, request, parms):
        return parms
