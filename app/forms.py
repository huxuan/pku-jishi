#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: forms.py
Author: huxuan
Email: i(at)huxuan.org
Description: forms used in app
"""

from flask.ext.wtf import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

class LoginForm(Form):
    """docstring for LoginForm"""
    email = StringField(u'邮箱', [
        validators.Email(),
        validators.InputRequired(),
    ])
    password = PasswordField(u'密码', [
        validators.InputRequired(),
    ])
    remember_me = BooleanField(u'记住我', [
        validators.Optional(),
    ])
