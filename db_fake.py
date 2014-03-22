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
        for status in xrange(2):
            fake_location_category(order, status)
    db.session.commit()

def fake_user_status(user, status):
    """docstring for fake_user_status"""
    if status != 0:
        user += str(status)
    u = models.User(
        email = user + '@pku.edu.cn',
        name = user,
        password = hashlib.md5(user).hexdigest(),
        avatar = '',
        phone = '13601156789',
        qq = '498877765',
        create_time = datetime.datetime.now(),
        status = status,
    )
    db.session.add(u)
    db.session.flush()
    t = lib.create_token(u)
    db.session.add(t)

def fake_user():
    """docstring for fake_user"""
    for user in USER:
        for status in xrange(3):
            fake_user_status(user, status)
    db.session.commit()

def fake_sell_status_price(user, category, location, status, price):
    """docstring for fake_sell_status_price"""
    create_time = datetime.datetime.now()
    valid_time = create_time + datetime.timedelta(random.randint(1, 10))
    title = '-'.join([
        category.name, location.name, user.name, str(status), str(price)])
    print 'sell:', title
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
    s.images, s.thumbnails = lib.images_encode(images_sell, s.id, [])

def fake_sell():
    """docstring for fake_sell"""
    for category in lib.get_categories(statuses=[0, 1]):
        for location in lib.get_locations(statuses=[0, 1]):
            for user in lib.get_users(statuses=[0, 1, 2]):
                for status in xrange(6):
                    fake_sell_status_price(user, category, location, status, 0)
                    fake_sell_status_price(user, category, location, status, random.randint(1, 100))
    db.session.commit()

def fake_buy_status(user, category, location, status):
    """docstring for fake_buy_status"""
    create_time = datetime.datetime.now()
    valid_time = create_time + datetime.timedelta(random.randint(1, 10))
    price_low = random.randint(0, 100)
    price_high = random.randint(price_low, 200)
    title = '-'.join([category.name, location.name, user.name, str(status)])
    print 'buy:', title
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
    for category in lib.get_categories(statuses=[0, 1]):
        for location in lib.get_locations(statuses=[0, 1]):
            for user in lib.get_users(statuses=[0, 1, 2]):
                for status in xrange(5):
                    fake_buy_status(user, category, location, status)
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
