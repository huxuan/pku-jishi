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

from app import app
from app import models
from app import mail
from app import db

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

def create_sell(user_id, title, price, deprecate, category_id, location_id,
        description, phone, qq, valid):
    """docstring for create_sell"""
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
    sell.description = form.description.data
    sell.phone = form.phone.data
    sell.qq = form.qq.data
    sell.valid = sell.create_time + \
        datetime.timedelta(days=int(form.valid.data))
    return sell

def create_buy(user_id, title, price_low, price_high, category_id, location_id,
        description, phone, qq, valid):
    """docstring for create_buy"""
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
    buy.description = form.description.data
    buy.phone = form.phone.data
    buy.qq = form.qq.data
    buy.valid = buy.create_time + datetime.timedelta(days=form.valid.data)
    return buy

def set_password(user, password):
    """docstring for set_password"""
    user.password = hashlib.md5(password).hexdigest()

def images_encode(uploadset, id, images_files):
    """docstring for images_encode"""
    images = []
    if images_files and images_files[0]:
        for index in xrange(len(images_files)):
            name = '%d_%d_%d%s' % (id, index,
                random.randint(100000, 999999),
                os.path.splitext(images_files[index].filename)[-1])
            uploadset.save(images_files[index], name=name)
            images.append(name)
    return pickle.dumps(images)

def images_decode(uploadset, images):
    """docstring for images_decode"""
    return ['uploads/%s/%s' % (uploadset.name, x)
        for x in pickle.loads(str(images))]

def get_user_count():
    """docstring for get_user_count"""
    return db.session.query(models.User).count()

def get_locations(status=0):
    """docstring for get_locations"""
    return db.session.query(models.Location).filter_by(status=status).all()

def get_categories(status=0):
    """docstring for get_categories"""
    return db.session.query(models.Category).filter_by(status=status).all()

def get_category(id, status=0):
    """docstring for get_category"""
    return db.session.query(models.Category).get(id)

def get_sell_count():
    """docstring for get_sell_count"""
    return db.session.query(models.Sell).count()

def get_sell_by_id(id):
    """docstring for get_sell_by_id"""
    return db.session.query(models.Sell).get(id)

def get_sells_by_category(category, status=0):
    """docstring for get_sells_by_category"""
    return db.session.query(models.Sell).filter_by(category=category, status=status).all()

def get_sells_by_user(user, status=0):
    """docstring for get_sells_by_user"""
    return db.session.query(models.Sell).filter_by(user=user, status=status).all()

def get_sells_free(limit=4, status=0):
    """docstring for get_sells_free"""
    return db.session.query(models.Sell).filter_by(price=0, status=status).\
        order_by(models.Sell.create_time.desc()).limit(limit).all()

def get_sells_floors(categories, limit=4, status=0):
    """docstring for get_sells_floors"""
    floors = []
    for category in categories:
        floor = db.session.query(models.Sell).\
            filter_by(category=category, status=0).\
            order_by(models.Sell.create_time.desc())[:limit]
        floors.append(floor)
    return floors

def get_sells_q_cid_lid(q, category_id=0, location_id=0):
    """docstring for get_sells_q_cid_lid"""
    res = models.Sell.query.whoosh_search(q).filter_by(status=0)
    if category_id != 0:
        res = res.filter_by(category_id=category_id)
    if location_id != 0:
        res = res.filter_by(location_id=location_id)
    return res.all()

def get_buy_count():
    """docstring for get_buy_count"""
    return db.session.query(models.Buy).count()

def get_buy_by_id(id):
    """docstring for get_buy_by_id"""
    return db.session.query(models.Buy).get(id)

def get_buys_by_category(category, status=0):
    """docstring for get_buys_by_category"""
    return db.session.query(models.Buy).filter_by(category=category, status=status).all()

def get_buys_by_user(user, status=0):
    """docstring for get_buys_by_user"""
    return db.session.query(models.Buy).filter_by(user=user, status=status).all()

def get_buys_floors(categories, limit=4, status=0):
    """docstring for get_buys_floors"""
    floors = []
    for category in categories:
        floor = db.session.query(models.Buy).\
            filter_by(category=category, status=0).\
            order_by(models.Buy.create_time.desc())[:limit]
        floors.append(floor)
    return floors

def get_buys_q_cid_lid(q, category_id=0, location_id=0):
    """docstring for get_buys_q_cid_lid"""
    res = models.Buy.query.whoosh_search(q).filter_by(status=0)
    if category_id != 0:
        res = res.filter_by(category_id=category_id)
    if location_id != 0:
        res = res.filter_by(location_id=location_id)
    return res.all()
