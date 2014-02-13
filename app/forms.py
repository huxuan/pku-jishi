#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: forms.py
Author: huxuan
Email: i(at)huxuan.org
Description: forms used in app
"""

import hashlib

from flask.ext.wtf import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from app import models

LABEL_EMAIL = u'邮箱'
LABEL_PASSWORD = u'密码'
LABEL_REMEMBER_ME = u'记住我'

MSG_EMAIL_FORMAT_ERROR = u'邮箱格式错误'
MSG_EMAIL_REQUIRED = u'邮箱不能为空'
MSG_EMAIL_INVALID = u'用户无效'
MSG_EMAIL_NONEXIST = u'用户不存在'
MSG_PASSWD_REQUIRED = u'密码不能为空'
MSG_PASSWD_INVALID = u'密码错误'

class EmailValidation(object):
    """docstring for EmailValidation"""
    def __call__(self, form, field):
        user = models.User.query.filter_by(email=field.data).first()
        if not user:
            raise validators.StopValidation(MSG_EMAIL_NONEXIST)
        if user.status != 0:
            raise validators.StopValidation(MSG_EMAIL_INVALID)

class CorrespondToEmailPassword(object):
    """docstring for CorrespondToEmailPassword"""
    def __init__(self, email_fieldname):
        self.email_fieldname = email_fieldname

    def __call__(self, form, field):
        email = form[self.email_fieldname].data
        user = models.User.query.filter_by(email=email).first()
        password = hashlib.md5(field.data).hexdigest()
        if user and password != user.password:
            raise validators.StopValidation(MSG_PASSWD_INVALID)

class LoginForm(Form):
    """docstring for LoginForm"""
    email = StringField(LABEL_EMAIL, [
        validators.Email(MSG_EMAIL_FORMAT_ERROR),
        validators.InputRequired(MSG_EMAIL_REQUIRED),
        EmailValidation(),
    ])
    password = PasswordField(LABEL_PASSWORD, [
        validators.InputRequired(MSG_PASSWD_REQUIRED),
        CorrespondToEmailPassword('email'),
    ])
    remember_me = BooleanField(LABEL_REMEMBER_ME, [
        validators.Optional(),
    ])
