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
from flask.ext.wtf import RecaptchaField
from flask.ext.wtf import validators as ext_validators
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from app import models

LABEL_EMAIL = u'邮箱'
LABEL_EMAIL_REGISTER = u'注册邮箱'
LABEL_USERNAME = u'用户名'
LABEL_PASSWD = u'密码'
LABEL_PASSWD_CONFIRM = u'确认密码'
LABEL_REMEMBER = u'记住我'
LABEL_CAPTCHA = u'验证码'
LABEL_TOS = u'同意网站协议'

MSG_EMAIL_FORMAT_ERROR = u'邮箱格式错误'
MSG_EMAIL_REQUIRED = u'邮箱不能为空'
MSG_EMAIL_INVALID = u'用户无效'
MSG_EMAIL_NONEXIST = u'此邮箱不存在'
MSG_EMAIL_EXIST = u'此邮箱已注册'
MSG_EMAIL_PKU = u'请使用北大邮箱@pku.edu.cn注册'
MSG_USERNAME_REQUIRED = u'用户名不能为空'
MSG_USERNAME_EXIST = u'此用户名已存在'
MSG_USERNAME_LENGTH = u'用户名不得少于6个字符'
MSG_PASSWD_REQUIRED = u'密码不能为空'
MSG_PASSWD_INVALID = u'密码错误'
MSG_PASSWD_LENGTH = u'密码不得少于6个字符'
MSG_PASSWD_CONFIRM_REQUIRED = u'确认密码不能为空'
MSG_PASSWD_CONFIRM_EQUAL = u'密码和确认密码必须一致'
MSG_CAPTCHA = u'验证码错误'
MSG_TOS = u'必须同意网站协议方可注册'

DESC_EMAIL = u'*请使用北大邮箱@pku.edu.cn注册'
DESC_USERNAME = u'*请填写用户名，不少于6个字符'
DESC_PASSWD = u'*请设置密码，不少于6位'
DESC_PASSWD_CONFIRM = u'*请重复上面设置的密码'
DESC_CAPTCHA = u'*请输入图中显示的单词'

class EmailValidation(object):
    """docstring for EmailValidation"""
    def __call__(self, form, field):
        user = models.User.query.filter_by(email=field.data).first()
        if not user:
            raise validators.StopValidation(MSG_EMAIL_NONEXIST)
        if user.status > 1:
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

class RegisterEmailValidation(object):
    """docstring for RegisterEmailValidation"""
    def __call__(self, form, field):
        email = field.data
        if not email.endswith('@pku.edu.cn'):
            raise validators.StopValidation(MSG_EMAIL_PKU)
        user = models.User.query.filter_by(email=email).first()
        if user:
            raise validators.StopValidation(MSG_EMAIL_EXIST)

class RegisterUsernameValidation(object):
    """docstring for RegisterUsernameValidation"""
    def __call__(self, form, field):
        user = models.User.query.filter_by(name=field.data).first()
        if user:
            raise validators.StopValidation(MSG_USERNAME_EXIST)

class LoginForm(Form):
    """docstring for LoginForm"""
    email = StringField(LABEL_EMAIL, [
        validators.Email(MSG_EMAIL_FORMAT_ERROR),
        validators.InputRequired(MSG_EMAIL_REQUIRED),
        EmailValidation(),
    ])
    password = PasswordField(LABEL_PASSWD, [
        validators.InputRequired(MSG_PASSWD_REQUIRED),
        CorrespondToEmailPassword('email'),
    ])
    remember = BooleanField(LABEL_REMEMBER, [
        validators.Optional(),
    ])

class RegisterForm(Form):
    """docstring for RegisterForm"""
    email = StringField(LABEL_EMAIL_REGISTER, [
        validators.Email(MSG_EMAIL_FORMAT_ERROR),
        validators.InputRequired(MSG_EMAIL_REQUIRED),
        RegisterEmailValidation(), ],
        description = DESC_EMAIL,
    )
    username = StringField(LABEL_USERNAME, [
        validators.InputRequired(MSG_USERNAME_REQUIRED),
        validators.Length(min=6, message=MSG_USERNAME_LENGTH),
        RegisterUsernameValidation(), ],
        description = DESC_USERNAME,
    )
    password = PasswordField(LABEL_PASSWD, [
        validators.InputRequired(MSG_PASSWD_REQUIRED),
        validators.Length(min=6, message=MSG_PASSWD_LENGTH),
        validators.EqualTo('password_confirm', MSG_PASSWD_CONFIRM_EQUAL),],
        description = DESC_PASSWD,
    )
    password_confirm = PasswordField(LABEL_PASSWD_CONFIRM, [
        validators.InputRequired(MSG_PASSWD_CONFIRM_REQUIRED),],
        description = DESC_PASSWD_CONFIRM,
    )
    accept_tos = BooleanField(LABEL_TOS, [
        validators.InputRequired(MSG_TOS),],
        default = True,
    )
    recaptcha = RecaptchaField(LABEL_CAPTCHA, [
        ext_validators.Recaptcha(MSG_CAPTCHA),],
        description = DESC_CAPTCHA,
    )
