# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_item_search(self):
        """test service_item to search"""

        flag = "user"
        api = "service.item.search"
        current_page = 1
        search_info = json.dumps({
            "buy_date_start":"2018-05-17 16:54:00",
            "buy_date_end":"2018-05-17 16:54:59"
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_item_get(self):
        """test service_item to get"""

        flag = "user"
        api = "service.item.get"
        service_item_id = 1

        result = self.access_api(flag = flag, api = api, service_item_id = service_item_id)
        self.assertTrue('service_item_info' in result)
        print(result["service_item_info"])
'''
