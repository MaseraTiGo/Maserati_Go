# coding=UTF-8

'''
Created on 2016年8月24日

@author: Administrator
'''

# import python standard package

# import thread package

# import my project package
from tuoen.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crm_dev',
        'USER': 'bq',
        'PASSWORD': 'zxcde321BQ',
        'HOST': '192.168.3.250',
        'PORT': '5432',
    },
}

TEST_PORT = "8000"
