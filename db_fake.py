#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_fake.py
Author: huxuan
Email: i(at)huxuan.org
Description: script to create fake items in database
"""

import re
import pickle
import datetime
import hashlib
import random

from app import db
from app import models
from app import lib
from app import images_sell

CATEGORY = [
    u'电脑/手机/数码',
    u'家电/家具',
    u'美妆护肤',
    u'服饰鞋帽/箱包',
    u'图书音像',
    u'文体/健身/户外',
    u'娱乐展演票务',
    u'代步工具',
    u'日用百货/杂货',
    u'食品饮料',
    u'租赁服务',
    u'其他',
]

SUBCATEGORIES = [
    [u'笔记本', u'平板电脑', u'台式机', u'电脑配件', u'手机', u'单反/相机', u'移动硬盘/U盘', u'MP3/4', u'其他数码',],
    [u'洗衣机', u'空调', u'电视机', u'电冰箱', u'电风扇', u'电吹风', u'其他电器', u'家具', ],
    [u'女生美妆用品', u'女生护肤用品', u'男生洁面护肤用品', ],
    [u'女生服饰', u'女生鞋帽', u'女生箱包', u'男生服饰鞋帽', u'男生箱包', ],
    [u'教材/工具书', u'考研', u'GRE/雅思/托福', u'小说文学', u'音像制品', ],
    [u'乐器', u'体育用品', u'健身卡', u'游泳卡', u'户外用品', ],
    [u'电影票', u'演出票', u'优惠/团购券', u'其他票务', ],
    [u'自行车', u'电动车', u'配件/装备', ],
    [u'日用百货', u'杂货', ],
    [u'休闲食品', u'地方特产', u'饮料', ],
    [u'房屋租赁', u'房屋合租', u'其他产品出租', ],
    [u'其他分类', ],
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

def fake_category_order_parent_id(name, order, parent_id):
    """docstring for fake_category_order_parent_id"""
    c = lib.get_category_by_id(order)
    if c:
        c.name = name
        c.order = order
        c.parent_id = parent_id
        c.status = 0
    else:
        c = models.Category(
            name = name,
            order = order,
            parent_id = parent_id,
            status = 0,
        )
    db.session.add(c)

def fake_category_subcategory_new():
    """docstring for fake_category_subcategory_new"""
    categories = db.session.query(models.Category).all()
    for order in xrange(len(categories)):
        categories[order].name = order + 1
    db.session.commit()
    order = 0
    for name in CATEGORY:
        order += 1
        fake_category_order_parent_id(name, order, 0)
    parent_id = 0
    for subcategories in SUBCATEGORIES:
        parent_id += 1
        for subcategory in subcategories:
            order += 1
            fake_category_order_parent_id(subcategory, order, parent_id)
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

def images_repair():
    """docstring for images_repair"""
    for sell in db.session.query(models.Sell):
        pattern = re.compile(r'%d_.*?jpg' % sell.id)
        images = pattern.findall(sell.images)
        print images
        print repr(pickle.dumps(images))
        sell.images = pickle.dumps(images)
        print pickle.loads(sell.images)
        db.session.commit()

def main():
    """docstring for main"""
    #fake_category()
    #fake_category_subcategory_new()
    #fake_location()
    #fake_user()
    #fake_sell()
    #fake_buy()
    images_repair()

if __name__ == '__main__':
    main()
