#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.py
Author: huxuan
Email: i(at)huxuan.org
Description: config for app
"""

# mysql / sqlalchemy
SQLALCHEMY_DATABASE_URI = 'mysql://pkujishi:jishipku@localhost/pkujishi'

# flask-wtf
WTF_CSRF_ENABLED = True
SECRET_KEY = 'pku-jishi-sk'
RECAPTCHA_PUBLIC_KEY = '6Ld-ke4SAAAAAMfKFowFML-YcWmWH-ElDEiFT_lQ'
RECAPTCHA_PRIVATE_KEY = '6Ld-ke4SAAAAAJIgozOAfBd3ktLFnCxNeLvLJSGw'

# flask-whooshalchemy
WHOOSH_BASE = 'whoosh'
