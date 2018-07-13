# coding=UTF-8

import time

from model.models import Journal
from tuoen.sys.utils.common.split_page import Splitor


class JournalMiddleware(object):

    @classmethod
    def register(self, active, active_type, passive,\
                 passive_type, journal_type, record_detail, remark):
        print(active, passive)
        return Journal.create(active_uid = active.id, active_name = active.name, \
            active_type = active_type, passive_uid = passive.id, passive_name = passive.name, \
                passive_type = passive_type, journal_type = journal_type, \
                     record_detail = record_detail, remark = remark)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询日志列表"""
        journal_qs = Journal.search(**search_info)
        return Splitor(current_page, journal_qs)
