#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lib.py
Author: huxuan
Email: i(at)huxuan.org
Description: lib used in app
"""

import os.path
import datetime
import hashlib
import random
import base64
import cPickle as pickle
from threading import Thread

from flask import g
from flask import render_template
from flask.ext.mail import Message
from sqlalchemy import or_

from wheezy.captcha.image import captcha
from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text
from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp

from app import app
from app import models
from app import mail
from app import db

STATUS = {
    'user': {
        0: u'已认证',
        1: u'未认证',
        2: u'已封禁',
    },
    'sell': {
        0: u'出售中',
        1: u'已下架',
        2: u'已预订',
        3: u'已售出',
        4: u'不出售',
        5: u'已封禁',
    },
    'buy': {
        0: u'求购中',
        1: u'已下架',
        2: u'已购得',
        3: u'不求购',
        4: u'已封禁',
    },
    'category': {
        0: u'有效',
        1: u'无效',
    },
    'location': {
        0: u'有效',
        1: u'无效',
    },
}
NUM = {
    0: u'〇',
    1: u'一',
    2: u'二',
    3: u'③',
    4: u'四',
    5: u'⑤',
    6: u'六',
    7: u'七',
    8: u'八',
    9: u'⑨'
}

CAPTCHA_IMAGE = captcha(drawings=[
    background(),
    text(fonts=[
        'fonts/CourierNew-Bold.ttf',
        'fonts/LiberationMono-Bold.ttf'],
        drawings=[
            warp(),
            rotate(),
            offset()
        ]),
    curve(),
    noise(),
    smooth()
])

def generate_captcha(code):
    """docstring for generate_captcha"""
    return CAPTCHA_IMAGE(code)

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_mail(msg):
    """docstring for send_async_mail"""
    with app.app_context():
        mail.send(msg)

def send_mail(subject, recipients, body, html, sender=None):
    """docstring for send_mail"""
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=body,
        html=html,
        sender=sender,
    )
    send_async_mail(msg)

def send_activation_mail(user, url):
    """docstring for send_activation_mail"""
    subject = u'欢迎注册北大集市网'
    recipients = [user.email]
    context = {
        'user': user,
        'url': url,
    }
    body = render_template('mail/activation.txt', **context)
    html = render_template('mail/activation.html', **context)
    send_mail(subject, recipients, body, html)

def send_password_mail(user, url):
    """docstring for send_password_mail"""
    subject = u'重置北大集市网的密码'
    recipients = [user.email]
    context = {
        'user': user,
        'url': url,
    }
    body = render_template('mail/password.txt', **context)
    html = render_template('mail/password.html', **context)
    send_mail(subject, recipients, body, html)

def activation_token_encode(user_id, confirm):
    """docstring for activation_token_encode"""
    # TODO(huxuan): encode datetime.datetime.now() in token
    token = ['pkujishi', 'activation', str(user_id), str(confirm)]
    return base64.b64encode('#'.join(token))

def activation_token_decode(token):
    """docstring for activation_token_decode"""
    try:
        token = base64.b64decode(token).split('#')
        if len(token) == 4 and token[0] == 'pkujishi' and token[1] == 'activation':
            return token[-2], int(token[-1])
    except TypeError:
        pass
    return None, 0

def password_token_encode(user_id, confirm):
    """docstring for password_token_encode"""
    # TODO(huxuan): encode datetime.datetime.now() in token
    token = ['pkujishi', 'password', str(user_id), str(confirm)]
    return base64.b64encode('#'.join(token))

def password_token_decode(token):
    """docstring for password_token_decode"""
    try:
        token = base64.b64decode(token).split('#')
        if len(token) == 4 and token[0] == 'pkujishi' and token[1] == 'password':
            return token[-2], int(token[-1])
    except TypeError:
        pass
    return None, 0

def create_user(email, name, password):
    """docstring for create_user"""
    user = models.User(
        email = email,
        name = name,
        password = hashlib.md5(password).hexdigest(),
        avatar = '',
        phone = '',
        qq = '',
        create_time = datetime.datetime.now(),
        status = 1,
    )
    return user

def create_token(user):
    """docstring for create_token"""
    token = user.token or models.Token(user_id=user.id)
    token.confirm = random.randint(100000, 999999)
    token.create_time = datetime.datetime.now()
    return token

def create_sell(user_id, title, price, deprecate, category_id, subcategory_id,
        location_id, description, phone, qq, valid):
    """docstring for create_sell"""
    if subcategory_id != 0:
        category_id = subcategory_id
    sell = models.Sell(
        user_id = user_id,
        category_id = category_id,
        location_id = location_id,
        title = title,
        price = price,
        deprecate = deprecate,
        description = description,
        create_time = datetime.datetime.now(),
        valid_time = datetime.datetime.now() + datetime.timedelta(days=valid),
        status = 0,
        phone = phone,
        qq = qq,
    )
    return sell

def update_sell_from_form(sell, form):
    """docstring for update_sell_from_form"""
    sell.title = form.title.data
    sell.price = form.price.data
    sell.deprecate = form.deprecate.data
    sell.location_id = form.location_id.data
    sell.category_id = form.category_id.data
    if form.subcategory_id.data != 0:
        buy.category_id = form.subcategory_id.data
    sell.description = form.description.data
    sell.phone = form.phone.data
    sell.qq = form.qq.data
    sell.valid = sell.create_time + \
        datetime.timedelta(days=int(form.valid.data))
    return sell

def create_buy(user_id, title, price_low, price_high, category_id,
        subcategory_id, location_id, description, phone, qq, valid):
    """docstring for create_buy"""
    if subcategory_id != 0:
        category_id = subcategory_id
    buy = models.Buy(
        user_id = user_id,
        category_id = category_id,
        location_id = location_id,
        title = title,
        price_low = price_low,
        price_high = price_high,
        description = description,
        create_time = datetime.datetime.now(),
        valid_time = datetime.datetime.now() + datetime.timedelta(days=valid),
        status = 0,
        phone = phone,
        qq = qq,
    )
    return buy

def update_buy_from_form(buy, form):
    """docstring for update_buy_from_form"""
    buy.title = form.title.data
    buy.price_low = form.price_low.data
    buy.price_high = form.price_high.data
    buy.location_id = form.location_id.data
    buy.category_id = form.category_id.data
    if form.subcategory_id.data != 0:
        buy.category_id = form.subcategory_id.data
    buy.description = form.description.data
    buy.phone = form.phone.data
    buy.qq = form.qq.data
    buy.valid = buy.create_time + datetime.timedelta(days=form.valid.data)
    return buy

def set_password(user, password):
    """docstring for set_password"""
    user.password = hashlib.md5(password).hexdigest()

def number_encode(number):
    """encode phone number to chinese"""
    result = ""
    for i,c in enumerate(number):
        if NUM[int(c)]:
            result += NUM[int(c)]
        else:
            result += c
    return result

def images_encode(uploadset, id, images_files):
    """docstring for images_encode"""
    images_files = filter(None, images_files)
    images = []
    thumbnails = ''
    if images_files and images_files[0]:
        for index in xrange(len(images_files)):
            name = '%d_%d_%d%s' % (id, index,
                random.randint(100000, 999999),
                os.path.splitext(images_files[index].filename)[-1].lower())
            uploadset.save(images_files[index], name=name)
            images.append(name)
        thumbnails = images[0]
    return pickle.dumps(images), thumbnails

def images_decode(uploadset, images):
    """docstring for images_decode"""
    return ['uploads/%s/%s' % (uploadset.name, x)
        for x in pickle.loads(str(images))]

def get_user_count():
    """docstring for get_user_count"""
    return db.session.query(models.User).count()

def get_users(statuses=[0]):
    """docstring for get_users"""
    return db.session.query(models.User).\
        filter(models.User.status.in_(statuses)).all()

def get_user_by_id(id):
    """docstring for get_user"""
    return db.session.query(models.User).get(id)

def get_user_by_email(email):
    """docstring for get_user_by_email"""
    return db.session.query(models.User).filter_by(email=email).first()

def get_user_by_name(name):
    """docstring for get_user_by_name"""
    return db.session.query(models.User).filter_by(name=name).first()

def get_categories(statuses=[0]):
    """docstring for get_categories"""
    return db.session.query(models.Category).\
        filter_by(parent_id=0).\
        filter(models.Category.status.in_(statuses)).\
        order_by(models.Category.order).all()

def get_subcategories(statuses=[0]):
    """docstring for get_categories"""
    subcategories = db.session.query(models.Category).\
        filter(models.Category.parent_id!=0).\
        filter(models.Category.status.in_(statuses)).\
        order_by(models.Category.order).all()
    res = []
    for subcategory in subcategories:
        if not res or res[-1][-1].parent_id != subcategory.parent_id:
            res.append([])
        res[-1].append(subcategory)
    return res

def get_category(id):
    """docstring for get_category"""
    return db.session.query(models.Category).get(id)

def get_category_by_id(id):
    """docstring for get_category_by_id"""
    return get_category(id)

def get_category_by_name(name):
    """docstring for get_category_by_name"""
    return db.session.query(models.Category).filter_by(name=name).first()

def get_category_ids_from_category_id(category_id):
    """docstring for get_category_ids_from_id"""
    category_ids = [category_id, ]
    category = get_category_by_id(category_id)
    if category.parent_id != 0:
        category_ids.append(category.parent_id)
    return category_ids

def get_locations(statuses=[0]):
    """docstring for get_locations"""
    return db.session.query(models.Location).\
        filter(models.Location.status.in_(statuses)).all()

def get_location(id):
    """docstring for get_location"""
    return db.session.query(models.Location).get(id)

def get_sell_count():
    """docstring for get_sell_count"""
    return db.session.query(models.Sell).count()

def get_sell_by_id(id):
    """docstring for get_sell_by_id"""
    return db.session.query(models.Sell).get(id)

def get_sells(statuses=[0], price=-1, user_id=0, category_id=0, location_id=0,
        page=1, per_page=20):
    """docstring for get_sells"""
    sells = db.session.query(models.Sell)
    sells = statuses and sells.filter(models.Sell.status.in_(statuses)) or sells
    sells = price >= 0 and sells.filter_by(price=price) or sells
    sells = user_id and sells.filter_by(user_id=user_id) or \
        sells.filter(or_(models.Sell.user.has(status=0),
            models.Sell.user.has(status=1)))
    if category_id:
        category_ids = get_category_ids_from_category_id(category_id)
        sells = sells.filter(models.Sell.category_id.in_(category_ids))
    else:
        sells = sells.filter(models.Sell.category.has(status=0))
    sells = location_id and sells.filter_by(location_id=location_id) or \
        sells.filter(models.Sell.location.has(status=0))
    sells = sells.order_by(models.Sell.create_time.desc())
    total = sells.count()
    sells = sells.limit(per_page).offset((page - 1) * per_page)
    return total, sells.all()

def get_sells_floors(categories, page=1, per_page=4, **kwargs):
    """docstring for get_sells_floors"""
    floors = [
        get_sells(category_id=category.id, page=page, per_page=per_page,
            **kwargs)[1]
        for category in categories
    ]
    return floors

def get_sells_q_cid_lid(q, category_id=0, location_id=0, statuses=[0], page=1,
        per_page=20, limit=200):
    """docstring for get_sells_q_cid_lid"""
    res = models.Sell.query
    res = res.filter(or_(models.Sell.user.has(status=0),
        models.Sell.user.has(status=1)))
    res = statuses and res.filter(models.Sell.status.in_(statuses)) or res
    if category_id:
        category_ids = get_category_ids_from_category_id(category_id)
        res = res.filter(models.Sell.category_id.in_(category_ids))
    else:
        res = res.filter(models.Sell.category.has(status=0))
    res = location_id and res.filter_by(location_id=location_id) or \
            res.filter(models.Sell.location.has(status=0))
    res = res.whoosh_search(q)
    res = res.all()[:limit]
    total = len(res)
    res = res[(page - 1) * per_page: page * per_page]
    return total, res

def get_buy_count():
    """docstring for get_buy_count"""
    return db.session.query(models.Buy).count()

def get_buy_by_id(id):
    """docstring for get_buy_by_id"""
    return db.session.query(models.Buy).get(id)

def get_buys(statuses=[0], user_id=0, category_id=0, location_id=0, limit=1000,
        page=1, per_page=20):
    """docstring for get_buys"""
    buys = db.session.query(models.Buy)
    buys = statuses and buys.filter(models.Buy.status.in_(statuses)) or buys
    buys = user_id and buys.filter_by(user_id=user_id) or \
        buys.filter(or_(models.Buy.user.has(status=0),
            models.Buy.user.has(status=1)))
    if category_id:
        category_ids = get_category_ids_from_category_id(category_id)
        buys = buys.filter(models.Buy.category_id.in_(category_ids))
    else:
        buys = buys.filter(models.Buy.category.has(status=0))
    buys = location_id and buys.filter_by(location_id=location_id) or \
        buys.filter(models.Buy.location.has(status=0))
    buys = buys.order_by(models.Buy.create_time.desc())
    total = buys.count()
    buys = buys.limit(per_page).offset((page - 1) * per_page)
    return total, buys.all()

def get_buys_floors(categories, page=1, per_page=4, **kwargs):
    """docstring for get_buys_floors"""
    floors = [
        get_buys(category_id=category.id, page=page, per_page=per_page,
            **kwargs)[1]
        for category in categories
    ]
    return floors

def get_buys_q_cid_lid(q, category_id=0, location_id=0, statuses=[0], page=1,
        per_page=20, limit=200):
    """docstring for get_buys_q_cid_lid"""
    res = models.Buy.query
    res = res.filter(or_(models.Buy.user.has(status=0),
        models.Buy.user.has(status=1)))
    res = statuses and res.filter(models.Buy.status.in_(statuses)) or res
    if category_id:
        category_ids = get_category_ids_from_category_id(category_id)
        res = res.filter(models.Buy.category_id.in_(category_ids))
    else:
        res = res.filter(models.Buy.category.has(status=0))
    res = location_id and res.filter_by(location_id=location_id) or \
        res.filter(models.Buy.location.has(status=0))
    res = res.whoosh_search(q)
    res = res.all()[:limit]
    total = len(res)
    res = res[(page - 1) * per_page: page * per_page]
    return total, res
