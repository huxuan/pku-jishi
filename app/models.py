#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: models.py
Author: huxuan
Email: i(at)huxuan.org
Description: models used in app
"""

import sys
sys.path.insert(0, 'Flask-WhooshAlchemy')
import flask_whooshalchemy as whooshalchemy

from app import app
from app import db

class User(db.Model):
    """docstring for User"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    phone = db.Column(db.String(40))
    qq = db.Column(db.String(40))
    create_time = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    sells = db.relationship('Sell', backref='user', lazy='dynamic')
    buys = db.relationship('Buy', backref='user', lazy='dynamic')
    token = db.relationship('Token', backref='user', uselist=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status <= 1

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        """docstring for __repr__"""
        return '<User %r>' % self.name

class Category(db.Model):
    """docstring for Category"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    order = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)
    sells = db.relationship('Sell', backref='category', lazy='dynamic')
    buys = db.relationship('Buy', backref='category', lazy='dynamic')

    def __repr__(self):
        """docstring for __repr__"""
        return '<Category %r>' % self.name

class Location(db.Model):
    """docstring for location"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    order = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)
    sells = db.relationship('Sell', backref='location', lazy='dynamic')
    buys = db.relationship('Buy', backref='location', lazy='dynamic')

    def __repr__(self):
        """docstring for __repr__"""
        return '<Location %r>' % self.name

class Sell(db.Model):
    """docstring for Sell"""
    __searchable__ = ['title', 'description']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    title = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    images = db.Column(db.String(255))
    deprecate = db.Column(db.SmallInteger)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    valid_time = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    phone = db.Column(db.String(40))
    qq = db.Column(db.String(40))

    def __repr__(self):
        """docstring for __repr__"""
        return '<Sell id:%r user_id:%r title:%r>' % (self.id, self.user_id,
                self.title)

class Buy(db.Model):
    """docstring for Buy"""
    __searchable__ = ['title', 'description']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    title = db.Column(db.String(30), nullable=False)
    price_low = db.Column(db.Integer)
    price_high = db.Column(db.Integer)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    valid_time = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    phone = db.Column(db.String(40))
    qq = db.Column(db.String(40))

    def __repr__(self):
        """docstring for __repr__"""
        return '<Buy id:%r user_id:%r title:%r>' % (self.id, self.user_id,
                self.title)

class Token(db.Model):
    """docstring for Token"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    confirm = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """docstring for __repr__"""
        return '<Token user_id:%r confirm:%r create_time:%r>' % (self.user_id,
            self.confirm, self.create_time)

whooshalchemy.whoosh_index(app, Sell)
whooshalchemy.whoosh_index(app, Buy)
