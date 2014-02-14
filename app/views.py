#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user

from app import app
from app import lib
from app import forms
from app import models
from app import login_manager

MSG_LOGIN_SUCCESS = u'登录成功！'
MSG_REGISTER_SUCCESS = u'注册成功！'

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"

@login_manager.user_loader
def load_user(id):
    """docstring for load_user"""
    return models.User.query.get(int(id))

@app.before_request
def before_request():
    """docstring for before_request"""
    g.user = current_user

@app.route('/')
def index():
    """docstring for index"""
    context = {}
    context['categories'] = models.Category.query.\
            filter_by(status=0).all()
    context['sells_free'] = models.Sell.query.\
        filter_by(price=0, status=0).\
        order_by(models.Sell.create_time.desc()).\
        limit(4).all()
    context['sells_floors'] = []
    for category in context['categories']:
        sells_floor = models.Sell.query.\
            filter_by(category=category, status=0).\
            order_by(models.Sell.create_time.desc()).\
            limit(4).all()
        context['sells_floors'].append(sells_floor)
    context['user_count'] = models.User.query.count()
    context['sell_count'] = models.Sell.query.count()
    context['buy_count'] = models.Buy.query.count()
    return render_template("index.html", **context)

@app.route('/user/login', methods=('GET', 'POST'))
def user_login():
    """docstring for user_login"""
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))
    context = {}
    context['form'] = forms.LoginForm()
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        user = models.User.query.filter_by(email=email).first()
        remember = context['form'].remember.data
        login_user(user, remember=remember)
        flash(MSG_LOGIN_SUCCESS)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template("user/login.html", **context)

@app.route("/user/logout")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@app.route('/user/register', methods=('GET', 'POST'))
def user_register():
    """docstring for user_register"""
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))
    context = {}
    context['form'] = forms.RegisterForm()
    if context['form'].validate_on_submit():
        lib.create_user(
            email = context['form'].email.data,
            name = context['form'].username.data,
            password = context['form'].password.data,
        )
        flash(MSG_REGISTER_SUCCESS)
        return redirect(url_for('user_login'))
    return render_template("user/register.html", **context)

@app.route('/user/resend_confirm_mail')
@login_required
def user_resend_confirm_mail():
    """docstring for user_resend_confirm_mail"""
    return render_template("user/resend_confirm_mail.html",
        )

@app.route('/user/forget_password')
@login_required
def user_forget_password():
    """docstring for user_forget_password"""
    return render_template("user/forget_password.html",
        )

@app.route('/user/reset_password')
@login_required
def user_reset_password():
    """docstring for user_reset_password"""
    return render_template("user/reset_password.html",
        )

@app.route('/user/change_password')
@login_required
def user_change_password():
    """docstring for user_change_password"""
    return render_template("user/change_password.html",
        )

@app.route('/user/sell')
@login_required
def user_sell():
    """docstring for user_sell"""
    return render_template("user/sell.html",
            )

@app.route('/user/buy')
@login_required
def user_buy():
    """docstring for user_buy"""
    return render_template("user/buy.html",
        )

@app.route('/user/index')
@login_required
def user_index():
    """docstring for user_index"""
    return render_template("user/index.html",
        )

@app.route('/user/<int:id>')
@login_required
def user_id(id):
    """docstring for user_id"""
    return render_template("user/index.html",
        )

@app.route('/user/message')
@login_required
def user_message():
    """docstring for user_message"""
    return render_template("user/message.html",
        )

@app.route('/user/info')
@login_required
def user_info():
    """docstring for user_info"""
    return render_template("user/info.html",
        )

@app.route('/user/info/edit')
@login_required
def user_info_edit():
    """docstring for user_info_edit"""
    context = {}
    return render_template("user/info_edit.html",**context)

@app.route('/sell/category/<int:id>')
def sell_category_id(id):
    """docstring for sell_category_id"""
    context = {}
    context['categories'] = models.Category.query.\
            filter_by(status=0).all()
    context['category'] = models.Category.query.\
            filter_by(id=id).first()
    context['sells_floor'] = models.Sell.query.\
            filter_by(category_id=id, status=0).\
            order_by(models.Sell.create_time.desc()).all()
    return render_template("sell/category.html", **context)

@app.route('/sell/<int:id>')
def sell_id(id):
    """docstring for sell_id"""
    context = {}
    return render_template("sell/detail.html", **context)

@app.route('/sell/edit/<int:id>')
@login_required
def sell_edit_id(id):
    """docstring for sell_detail_id"""
    context = {}
    return render_template("sell/detail_edit.html", **context)

@app.route('/sell/post')
@login_required
def sell_post():
    """docstring for sell_post"""
    return render_template("sell/post.html",
        )

@app.route('/buy/')
def buy():
    """docstring for buy_category_id"""
    context = {}
    context['categories'] = models.Category.query.\
            filter_by(status=0).all()
    return render_template("buy/index.html", **context)

@app.route('/buy/category/<int:id>')
def buy_category_id(id):
    """docstring for buy_category_id"""
    context = {}
    context['categories'] = models.Category.query.\
            filter_by(status=0).all()
    return render_template("buy/category.html", **context)

@app.route('/buy/<int:id>')
def buy_id(id):
    """docstring for buy_id"""
    context = {}
    return render_template("buy/detail.html", **context)

@app.route('/buy/edit/<int:id>')
@login_required
def buy_edit_id(id):
    """docstring for buy_edit_id"""
    context = {}
    return render_template("buy/detail_edit.html", **context)

@app.route('/buy/post')
@login_required
def buy_post():
    """docstring for buy_post"""
    return render_template("buy/post.html",
        )

@app.route('/search')
def search():
    """docstring for search"""
    return render_template("search.html",
        )
