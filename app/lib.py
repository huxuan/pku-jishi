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

from app import models

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

def get_user_count():
    """docstring for get_user_count"""
    return models.User.query.count()

def get_locations(status=0):
    """docstring for get_locations"""
    return models.Location.query.filter_by(status=status).all()

def get_categories(status=0):
    """docstring for get_categories"""
    return models.Category.query.filter_by(status=status).all()

def get_category(id, status=0):
    """docstring for get_category"""
    return models.Category.query.get(id)

def get_sell_count():
    """docstring for get_sell_count"""
    return models.Sell.query.count()

def get_sell_by_id(id):
    """docstring for get_sell_by_id"""
    return models.Sell.query.get(id)

def get_sells_by_category(category, status=0):
    """docstring for get_sells_by_category"""
    return models.Sell.query.filter_by(category=category, status=status).all()

def get_sells_by_user(user, status=0):
    """docstring for get_sells_by_user"""
    return models.Sell.query.filter_by(user=user, status=status).all()

def get_sells_free(limit=4, status=0):
    """docstring for get_sells_free"""
    return models.Sell.query.filter_by(price=0, status=status).\
        order_by(models.Sell.create_time.desc()).limit(limit).all()

def get_sells_floors(categories, limit=4, status=0):
    """docstring for get_sells_floors"""
    floors = []
    for category in categories:
        floor = models.Sell.query.\
            filter_by(category=category, status=0).\
            order_by(models.Sell.create_time.desc()).\
            limit(limit).all()
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
    return models.Buy.query.count()

def get_buy_by_id(id):
    """docstring for get_buy_by_id"""
    return models.Buy.query.get(id)

def get_buys_by_category(category, status=0):
    """docstring for get_buys_by_category"""
    return models.Buy.query.filter_by(category=category, status=status).all()

def get_buys_by_user(user, status=0):
    """docstring for get_buys_by_user"""
    return models.Buy.query.filter_by(user=user, status=status).all()

def get_buys_floors(categories, limit=4, status=0):
    """docstring for get_buys_floors"""
    floors = []
    for category in categories:
        floor = models.Buy.query.\
            filter_by(category=category, status=0).\
            order_by(models.Buy.create_time.desc()).\
            limit(limit).all()
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
