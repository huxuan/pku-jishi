#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lib.py
Author: huxuan
Email: i(at)huxuan.org
Description: lib used in app
"""

import datetime
import hashlib
import random
import cPickle as pickle

from flask import g

from app import models
from app import db

def create_user(email, name, password):
    """docstring for create_user"""
    user = models.User(
        email = email,
        name = name,
        password = hashlib.md5(password).hexdigest(),
        confirm = random.randint(100000, 999999),
        avatar = '',
        phone = '',
        qq = '',
        create_time = datetime.datetime.now(),
        status = 1,
    )
    return user

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

def set_password(password):
    """docstring for set_password"""
    g.user.password = hashlib.md5(password).hexdigest()

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
    res = db.session.query(models.Sell).whoosh_search(q).filter_by(status=0)
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
    res = db.session.query(models.Buy).whoosh_search(q).filter_by(status=0)
    if category_id != 0:
        res = res.filter_by(category_id=category_id)
    if location_id != 0:
        res = res.filter_by(location_id=location_id)
    return res.all()
