#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_fake.py
Author: huxuan
Email: i(at)huxuan.org
Description: script to create fake items in database
"""

import datetime
import hashlib
import random

from app import db
from app import models
from app import lib
from app import images_sell

CATEGORY = [
    u'代步工具',
    u'电脑办公',
    u'手机数码',
    u'图书音像',
    u'运动健身',
    u'日用产品',
    u'衣服鞋帽',
    u'娱乐票务',
    u'电器产品',
    u'房屋租赁',
    u'食品饮料',
    u'其他分类',
]

LOCATION = [
    u'北大本部',
    u'北大医学部',
    u'北大大兴校区',
    u'北大深研院',
]

USER = [
    'xuan.hu',
    'qiangrw',
    'guyue',
]

def fake_category_status(order, status):
    """docstring for fake_category_status"""
    name = CATEGORY[order]
    if status != 0:
        name += unicode(status)
    c = models.Category(
        name = name,
        order = order + 1,
        parent_id = 0,
        status = status,
    )
    db.session.add(c)

def fake_category():
    """docstring for fake_category"""
    for order in xrange(len(CATEGORY)):
        fake_category_status(order, 0)
        fake_category_status(order, 1)
    db.session.commit()

def fake_location_category(order, status):
    """docstring for fake_location_category"""
    name = LOCATION[order]
    if status != 0:
        name += unicode(status)
    l = models.Location(
        name = name,
        order = order + 1,
        status = status,
    )
    db.session.add(l)

def fake_location():
    """docstring for fake_location"""
    for order in xrange(len(LOCATION)):
        fake_location_category(order, 0)
        fake_location_category(order, 1)
    db.session.commit()

def fake_user_status(user, status):
    """docstring for fake_user_status"""
    if status != 0:
        user = user + str(status)
    u = models.User(
        email = user + '@pku.edu.cn',
        name = user,
        password = hashlib.md5(user).hexdigest(),
        confirm = random.randint(100000, 999999),
        avatar = '',
        phone = '13601156789',
        qq = '498877765',
        create_time = datetime.datetime.now(),
        status = status,
    )
    db.session.add(u)

def fake_user():
    """docstring for fake_user"""
    for user in USER:
        fake_user_status(user, 0)
        fake_user_status(user, 1)
        fake_user_status(user, 2)
    db.session.commit()

def fake_sell_status_price(category, location, status, price):
    """docstring for fake_sell_status_price"""
    user_name = USER[random.randint(0, len(USER) - 1)]
    user = models.User.query.filter_by(name = user_name).first()
    create_time = datetime.datetime.now()
    valid_time = create_time + datetime.timedelta(random.randint(1, 10))
    title = '-'.join([
        category.name, location.name, user_name, str(status), str(price)])
    s = models.Sell(
        user_id = user.id,
        category_id = category.id,
        location_id = location.id,
        title = title,
        price = price,
        deprecate = random.randint(1, 10),
        description = title * 5,
        create_time = create_time,
        valid_time = valid_time,
        qq = '491677777',
        phone = '13601178890',
        status = status,
    )
    db.session.add(s)
    db.session.flush()
    s.images = lib.images_encode(images_sell, s.id, [])

def fake_sell():
    """docstring for fake_sell"""
    for category_name in CATEGORY:
        category = models.Category.query.filter_by(name = category_name).first()
        for location_name in LOCATION:
            location = models.Location.query.filter_by(name = location_name).first()
            fake_sell_status_price(category, location, 0, 0)
            fake_sell_status_price(category, location, 0, random.randint(1, 100))
            fake_sell_status_price(category, location, 1, 0)
            fake_sell_status_price(category, location, 1, random.randint(1, 100))
            fake_sell_status_price(category, location, 2, 0)
            fake_sell_status_price(category, location, 2, random.randint(1, 100))
    db.session.commit()

def fake_buy_status(category, location, status):
    """docstring for fake_buy_status"""
    user_name = USER[random.randint(0, len(USER) - 1)]
    user = models.User.query.filter_by(name = user_name).first()
    create_time = datetime.datetime.now()
    valid_time = create_time + datetime.timedelta(random.randint(1, 10))
    price_low = random.randint(0, 100)
    price_high = random.randint(price_low, 200)
    title = '-'.join([category.name, location.name, user_name, str(status)])
    s = models.Buy(
        user_id = user.id,
        category_id = category.id,
        location_id = location.id,
        title = title,
        price_low = price_low,
        price_high = price_high,
        description = title * 5,
        create_time = create_time,
        valid_time = valid_time,
        phone = '13601198877',
        qq = '491617788',
        status = status,
    )
    db.session.add(s)

def fake_buy():
    """docstring for fake_buy"""
    for category_name in CATEGORY:
        category = models.Category.query.filter_by(name = category_name).first()
        for location_name in LOCATION:
            location = models.Location.query.filter_by(name = location_name).first()
            fake_buy_status(category, location, 0)
            fake_buy_status(category, location, 1)
            fake_buy_status(category, location, 2)
    db.session.commit()

def main():
    """docstring for main"""
    fake_category()
    fake_location()
    fake_user()
    fake_sell()
    fake_buy()

if __name__ == '__main__':
    main()
