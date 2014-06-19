#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.py
Author: huxuan
Email: i(at)huxuan.org
Description: config for app
"""
# Custom
DEFAULT_USER_STATUS = 0

# mysql / sqlalchemy
SQLALCHEMY_DATABASE_URI = 'mysql://pkujishi:jishipku@localhost/pkujishi'

# flask-wtf
WTF_CSRF_ENABLED = True
SECRET_KEY = 'pku-jishi-sk'

# flask-whooshalchemy
WHOOSH_BASE = 'whoosh'
from jieba.analyse import ChineseAnalyzer
WHOOSH_ANALYZER = ChineseAnalyzer()

# flask-uploads
UPLOADS_DEFAULT_DEST = 'app/static/uploads/'

# flask-mail
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'no-reply@pkujishi.com'
MAIL_PASSWORD = 'pkujishi.com'
MAIL_DEFAULT_SENDER = 'no-reply@pkujishi.com'

# flask-images
SECRET_KEY = 'monkey'
IMAGES_PATH = ['static']
IMAGES_CACHE = '/alidata1/Code/pku-jishi/app/static/flask-images'

# flask-paginate
PER_PAGE = 20
