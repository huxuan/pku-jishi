#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

import hashlib

from flask import render_template
from flask import request
from flask import redirect
from app import app
from app import forms
from models import User
from models import Category
from models import Sell
from models import Buy

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"

@app.route('/')
def index():
    """docstring for index"""
    context = {}
    context['categories'] = Category.query.\
            filter_by(status=0).all()
    context['sells_free'] = Sell.query.\
        filter_by(price=0, status=0).\
        order_by(Sell.create_time.desc()).\
        limit(4).all()
    context['sells_floors'] = []
    for category in context['categories']:
        sells_floor = Sell.query.\
            filter_by(category=category, status=0).\
            order_by(Sell.create_time.desc()).\
            limit(4).all()
        context['sells_floors'].append(sells_floor)
    context['user_count'] = User.query.count()
    context['sell_count'] = Sell.query.count()
    context['buy_count'] = Buy.query.count()
    print '#' * 80
    print context
    print '#' * 80
    return render_template("index.html", **context)

@app.route('/notes')
def notes():
    """docstring for notes"""
    return render_template("notes.html",
        )

@app.route('/user/login', methods=('GET', 'POST'))
def user_login():
    """docstring for user_login"""
    context = {}
    context['url'] = request.args.get('url', '/')
    context['form'] = forms.LoginForm()
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        password = hashlib.md5(context['form'].password.data).hexdigest()
        user = User.query.filter_by(email=email, status=0). first()
        if user:
            if user.password == password:
                return redirect(context['url'])
            else:
                context['error_msg'] = u'密码错误'
        else:
            context['error_msg'] = u'用户不存在'
    return render_template("user/login.html", **context)

@app.route('/user/register')
def user_register():
    """docstring for user_register"""
    return render_template("user/register.html",
        )

@app.route('/user/resend_confirm_mail')
def user_resend_confirm_mail():
    """docstring for user_resend_confirm_mail"""
    return render_template("user/resend_confirm_mail.html",
        )

@app.route('/user/forget_password')
def user_forget_password():
    """docstring for user_forget_password"""
    return render_template("user/forget_password.html",
        )

@app.route('/user/reset_password')
def user_reset_password():
    """docstring for user_reset_password"""
    return render_template("user/reset_password.html",
        )

@app.route('/user/change_password')
def user_change_password():
    """docstring for user_change_password"""
    return render_template("user/change_password.html",
        )

@app.route('/user/sell')
def user_sell():
    """docstring for user_sell"""
    return render_template("user/sell.html",
            )

@app.route('/user/buy')
def user_buy():
    """docstring for user_buy"""
    return render_template("user/buy.html",
        )

@app.route('/user/index')
def user_index():
    """docstring for user_index"""
    return render_template("user/index.html",
        )

def user_id(id):
    """docstring for user_id"""
    return render_template("user/index.html",
        )


@app.route('/user/message')
def user_message():
    """docstring for user_message"""
    return render_template("user/message.html",
        )

@app.route('/user/info')
def user_info():
    """docstring for user_info"""
    return render_template("user/info.html",
        )

@app.route('/user/info/edit')
def user_info_edit():
    """docstring for user_info_edit"""
    context = {}
    return render_template("user/info_edit.html",**context)

@app.route('/sell/category/<int:id>')
def sell_category_id(id):
    """docstring for sell_category_id"""
    context = {}
    context['categories'] = Category.query.\
            filter_by(status=0).all()
    context['category'] = Category.query.\
            filter_by(id=id).first()
    context['sells_floor'] = Sell.query.\
            filter_by(category_id=id, status=0).\
            order_by(Sell.create_time.desc()).all()
    return render_template("sell/category.html", **context)

@app.route('/sell/<int:id>')
def sell_id(id):
    """docstring for sell_id"""
    context = {}
    return render_template("sell/detail.html", **context)

@app.route('/sell/edit/<int:id>')
def sell_edit_id(id):
    """docstring for sell_detail_id"""
    context = {}
    return render_template("sell/detail_edit.html", **context)

@app.route('/sell/post')
def sell_post():
    """docstring for sell_post"""
    return render_template("sell/post.html",
        )

@app.route('/buy/')
def buy():
    """docstring for buy_category_id"""
    context = {}
    context['categories'] = Category.query.\
            filter_by(status=0).all()
    return render_template("buy/index.html", **context)

@app.route('/buy/category/<int:id>')
def buy_category_id(id):
    """docstring for buy_category_id"""
    context = {}
    context['categories'] = Category.query.\
            filter_by(status=0).all()
    return render_template("buy/category.html", **context)

@app.route('/buy/<int:id>')
def buy_id(id):
    """docstring for buy_id"""
    context = {}
    return render_template("buy/detail.html", **context)

@app.route('/buy/edit/<int:id>')
def buy_edit_id(id):
    """docstring for buy_edit_id"""
    context = {}
    return render_template("buy/detail_edit.html", **context)

@app.route('/buy/post')
def buy_post():
    """docstring for buy_post"""
    return render_template("buy/post.html",
        )

@app.route('/search/<q>')
def search(q):
    """docstring for search"""
    return render_template("search.html",
        )
