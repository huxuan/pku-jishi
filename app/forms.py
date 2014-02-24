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
from flask.ext.wtf.file import FileField
from flask.ext.wtf.file import FileAllowed
from flask.ext.wtf import validators as ext_validators
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import TextAreaField
from wtforms import validators

from app import models
from app import lib
from app import images_avatar
from app import images_sell

LEN_MAX_NAME = 30

LABEL_EMAIL = u'邮箱'
LABEL_EMAIL_REGISTER = u'注册邮箱'
LABEL_USERNAME = u'用户名'
LABEL_PASSWD = u'密码'
LABEL_PASSWD_CONFIRM = u'确认密码'
LABEL_REMEMBER = u'记住我'
LABEL_CAPTCHA = u'验证码'
LABEL_TOS = u'同意网站协议'
LABEL_TITLE = u'标题'
LABEL_IMAGES = u'商品图片'
LABEL_PRICE = u'商品价格'
LABEL_DEPRECATE = u'新旧程度'
LABEL_CATEGORY = u'商品分类'
LABEL_LOCATION = u'交易地点'
LABEL_DESCRIPTION = u'商品详情'
LABEL_PHONE = u'联系手机'
LABEL_QQ = u'联系QQ'
LABEL_VALID = u'有效时间'
LABEL_PRICE_RANGE = u'出价范围'

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
MSG_TITLE_REQUIRED = u'标题不能为空'
MSG_TITLE_LENGTH = u'标题不得多于%d个字符' % LEN_MAX_NAME
MSG_IMAGE_ALLOW = u'必须上传图片格式'
MSG_PRICE_REQUIRED = u'商品价格不能为空'
MSG_PRICE_NOT_DIGIT = u'商品价格必须是正整数'
MSG_PRICE_INVALID = u'商品价格不能为负数'
MSG_DEPRECATE_REQUIRED = u'新旧程度不能为空'
MSG_CATEGORY_REQUIRED = u'商品分类不能为空'
MSG_LOCATION_REQUIRED = u'交易地点不能为空'
MSG_DESCRIPTION_REQUIRED = u'商品详情不能为空'
MSG_PHONE_INVALID = u'请输入正确的手机号码'
MSG_QQ_INVALID = u'请输入正确的QQ号'
MSG_VALID_REQUIRED = u'有效时间不能为空'
MSG_PRICE_LOW_REQUIRED = u'最低价格不能为空'
MSG_PRICE_HIGH_REQUIRED = u'最高价格不能为空'

DESC_EMAIL = u'*请使用北大邮箱@pku.edu.cn注册'
DESC_USERNAME = u'*请填写用户名，不少于6个字符'
DESC_PASSWD = u'*请设置密码，不少于6位'
DESC_PASSWD_CONFIRM = u'*请重复上面设置的密码'
DESC_CAPTCHA = u'*请输入图中显示的单词'
DESC_VALID = u'天后自动下架（可在我的个人主页中重新发布）'
DESC_PRICE_LOW = u'最低价格'
DESC_PRICE_HIGH = u'最高价格'

RE_PHONE = u'(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0-9])\d{8}'
RE_QQ = u'[1-9][0-9]{4,}'

CHOICE_DEPRECATED = [
    (10, u'全新(10)'),
    (9, u'9'),
    (8, u'8'),
    (7, u'7'),
    (6, u'6'),
    (5, u'5'),
    (4, u'4'),
    (3, u'3'),
    (2, u'2'),
    (1, u'1'),
]
CHOICE_VALID = [
    (x, unicode(x))
    for x in range(1, 30)
]

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

class PriceValidation(object):
    """docstring for PriceValidation"""
    def __call__(self, form, field):
        if not field.data.isdigit():
            raise validators.StopValidation(MSG_PRICE_NOT_DIGIT)
        if int(field.data) < 0:
            raise validators.StopValidation(MSG_PRICE_INVALID)

class SellForm(Form):
    """docstring for SellForm"""
    title = StringField(LABEL_TITLE, [
        validators.InputRequired(MSG_TITLE_REQUIRED),
        validators.length(max=LEN_MAX_NAME, message=MSG_TITLE_LENGTH),],
    )
    images = FileField(LABEL_IMAGES, [
        FileAllowed(images_sell, MSG_IMAGE_ALLOW),],
    )
    price = StringField(LABEL_PRICE, [
        validators.InputRequired(MSG_PRICE_REQUIRED),
        PriceValidation(),
    ])
    deprecate = SelectField(LABEL_DEPRECATE, [
        validators.InputRequired(MSG_DEPRECATE_REQUIRED),],
        choices=CHOICE_DEPRECATED,
        coerce=int,
    )
    category = SelectField(LABEL_CATEGORY, [
        validators.InputRequired(MSG_CATEGORY_REQUIRED),],
        choices=[(x.id, x.name) for x in lib.get_categories()],
        coerce=int,
    )
    location = SelectField(LABEL_LOCATION, [
        validators.InputRequired(MSG_LOCATION_REQUIRED),],
        choices=[(x.id, x.name) for x in lib.get_locations()],
        coerce=int,
    )
    description = TextAreaField(LABEL_DESCRIPTION, [
        validators.InputRequired(MSG_DESCRIPTION_REQUIRED),],
    )
    phone = StringField(LABEL_PHONE, [
        validators.Regexp(RE_PHONE, message=MSG_PHONE_INVALID),],
    )
    qq = StringField(LABEL_QQ, [
        validators.Regexp(RE_QQ, message=MSG_QQ_INVALID),],
    )
    valid = SelectField(LABEL_VALID, [
        validators.InputRequired(MSG_VALID_REQUIRED),],
        description=DESC_VALID,
        choices=CHOICE_VALID,
        coerce=int,
        default=7,
    )

class BuyForm(Form):
    """docstring for BuyForm"""
    title = StringField(LABEL_TITLE, [
        validators.InputRequired(MSG_TITLE_REQUIRED),
        validators.length(max=LEN_MAX_NAME, message=MSG_TITLE_LENGTH),],
    )
    price_low = StringField(LABEL_PRICE_RANGE, [
        validators.InputRequired(MSG_PRICE_LOW_REQUIRED),
        PriceValidation(),],
        description=DESC_PRICE_LOW,
    )
    price_high = StringField(LABEL_PRICE_RANGE, [
        validators.InputRequired(MSG_PRICE_HIGH_REQUIRED),
        PriceValidation(),],
        description=DESC_PRICE_HIGH,
    )
    category = SelectField(LABEL_CATEGORY, [
        validators.InputRequired(MSG_CATEGORY_REQUIRED),],
        choices=[(x.id, x.name) for x in lib.get_categories()],
        coerce=int,
    )
    location = SelectField(LABEL_LOCATION, [
        validators.InputRequired(MSG_LOCATION_REQUIRED),],
        choices=[(x.id, x.name) for x in lib.get_locations()],
        coerce=int,
    )
    description = TextAreaField(LABEL_DESCRIPTION, [
        validators.InputRequired(MSG_DESCRIPTION_REQUIRED),],
    )
    phone = StringField(LABEL_PHONE, [
        validators.Regexp(RE_PHONE, message=MSG_PHONE_INVALID),],
    )
    qq = StringField(LABEL_QQ, [
        validators.Regexp(RE_QQ, message=MSG_QQ_INVALID),],
    )
    valid = SelectField(LABEL_VALID, [
        validators.InputRequired(MSG_VALID_REQUIRED),],
        description=DESC_VALID,
        choices=CHOICE_VALID,
        coerce=int,
        default=7,
    )
