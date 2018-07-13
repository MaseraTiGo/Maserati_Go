# -*- coding: utf-8 -*-
import json
import scrapy
from zhihu.items import ZhihuItem

class ZhihuuuSpider(scrapy.Spider):
    name = 'zhihuuu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    start_user = 'kaifulee'
    info_include = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.info_include), self.parse_user)
    
    def parse_user(self, response):
        with open('lkf.txt', 'w') as f:
            f.write(response.text)
        result = json.loads(response.text)
        item = ZhihuItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item        
            