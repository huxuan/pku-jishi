#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

import datetime
import random
import os.path
import cPickle as pickle

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
from flask.ext.paginate import Pagination

from app import app
from app import db
from app import lib
from app import forms
from app import models
from app import login_manager
from app import images_avatar
from app import images_sell

MSG_CATEGORY_SUCCESS = 'success'
MSG_CATEGORY_INFO = 'info'
MSG_CATEGORY_WARNING = 'warning'
MSG_CATEGORY_DANGER = 'danger'

MSG_LOGIN_REQUIRED = u'请登录后查看此页面'
MSG_LOGIN_SUCCESS = u'登录成功！'
MSG_REGISTER_SUCCESS = u'注册成功！'
MSG_USER_INVALID = u'此用户无效'
MSG_SELL_INVALID = u'此售出商品无效'
MSG_SELL_POST_SUCCESS = u'售出商品发布成功！'
MSG_BUY_INVALID = u'此求购商品无效'
MSG_BUY_POST_SUCCESS = u'求购商品发布成功！'

login_manager.login_view = 'user_login'
login_manager.login_message = MSG_LOGIN_REQUIRED
login_manager.login_message_category = MSG_CATEGORY_DANGER

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
    g.user_count = lib.get_user_count()
    g.sell_count = lib.get_sell_count()
    g.buy_count = lib.get_buy_count()

@app.route('/')
def index():
    """docstring for index"""
    context={
        'categories': lib.get_categories(status=0),
        'sells_free': lib.get_sells_free(limit=4, status=0),
    }
    context['sells_floors'] = lib.get_sells_floors(
        context['categories'], limit=4, status=0)
    return render_template("index.html", **context)

@app.route('/user/login', methods=('GET', 'POST'))
def user_login():
    """docstring for user_login"""
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))
    context={
        'form': forms.LoginForm(),
    }
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        user = models.User.query.filter_by(email=email).first()
        remember = context['form'].remember.data
        login_user(user, remember=remember)
        flash(MSG_LOGIN_SUCCESS, MSG_CATEGORY_SUCCESS)
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
        user = lib.create_user(
            email = context['form'].email.data,
            name = context['form'].username.data,
            password = context['form'].password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash(MSG_REGISTER_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_login'))
    return render_template("user/register.html", **context)

@app.route('/user/resend_confirm_mail')
@login_required
def user_resend_confirm_mail():
    """docstring for user_resend_confirm_mail"""
    # TODO(huxuan): form of resend_confirm_mail
    # TODO(qiangrw): entry of resend_confirm_mail
    return render_template("user/resend_confirm_mail.html",
        )

@app.route('/user/forget_password')
def user_forget_password():
    """docstring for user_forget_password"""
    # TODO(huxuan): form of user_forget_password
    return render_template("user/forget_password.html",
        )

@app.route('/user/reset_password')
def user_reset_password():
    """docstring for user_reset_password"""
    # TODO(huxuan): form of user_reset_password
    # TODO(qiangrw): entry of user_reset_password
    return render_template("user/reset_password.html",
        )

@app.route('/user/change_password')
@login_required
def user_change_password():
    """docstring for user_change_password"""
    # TODO(huxuan): form of user_change_password
    return render_template("user/change_password.html",
        )

@app.route('/user/sell')
@login_required
def user_sell():
    """docstring for user_sell"""
    context = {
        'sells': lib.get_sells_by_user(g.user, status=0)
    }
    return render_template("user/sell.html", **context)

@app.route('/user/buy')
@login_required
def user_buy():
    """docstring for user_buy"""
    context = {
        'buys': lib.get_buys_by_user(g.user),
    }
    return render_template("user/buy.html", **context)

@app.route('/user/index')
@login_required
def user_index():
    """docstring for user_index"""
    return redirect(url_for('user_id',id=g.user.id))

@app.route('/user/<int:id>')
def user_id(id):
    """docstring for user_id"""
    current_time = datetime.datetime.now()
    context = {}
    context['user'] = models.User.query.get(id)
    if not context['user'] or context['user'].status > 1:
        flash(MSG_USER_INVALID, MSG_CATEGORY_DANGER)
        return redirect(url_for('index'))
    context['sells'] = lib.get_sells_by_user(context['user'])
    return render_template("user/index.html", **context)

@app.route('/user/message')
@login_required
def user_message():
    """docstring for user_message"""
    context = {}
    return render_template("user/message.html", **context)

@app.route('/user/info')
@login_required
def user_info():
    """docstring for user_info"""
    context = {}
    return render_template("user/info.html", **context)

@app.route('/user/info/edit')
@login_required
def user_info_edit():
    """docstring for user_info_edit"""
    context = {}
    # TODO(huxuan): form of user_info_edit
    return render_template("user/info_edit.html", **context)

@app.route('/sell/category/<int:id>')
def sell_category_id(id):
    """docstring for sell_category_id"""
    page = int(request.args.get('page', 1))
    context = {
        'categories': lib.get_categories(status=0),
        'category': lib.get_category(id)
    }
    context['sells'] = lib.get_sells_by_category(context['category'])
    context['pagination'] = Pagination(page=page,
        total=len(context['sells']),
        record_name='sells',
    )
    return render_template("sell/category.html", **context)

@app.route('/sell/detail/<int:id>')
def sell_id(id):
    """docstring for sell_id"""
    context = {
        'sell': lib.get_sell_by_id(id),
    }
    context['images'] = ['uploads/sell/%s' % x
        for x in pickle.loads(str(context['sell'].images))]
    if context['sell'] and context['sell'].status <= 1:
        return render_template("sell/detail.html", **context)
    flash(MSG_SELL_INVALID, MSG_CATEGORY_DANGER)
    return redirect(url_for('index'))

@app.route('/sell/detail/edit/<int:id>')
@login_required
def sell_edit_id(id):
    """docstring for sell_edit_id"""
    context = {
        'sell': lib.get_sell_by_id(id),
    }
    # TODO(huxuan): form of sell_edit_id
    return render_template("sell/detail_edit.html", **context)

@app.route('/sell/detail/post', methods=('GET', 'POST'))
@login_required
def sell_post():
    """docstring for sell_post"""
    context = {
        'form': forms.SellForm(),
    }
    if context['form'].validate_on_submit():
        sell = lib.create_sell(
            user_id = g.user.id,
            title = context['form'].title.data,
            price = context['form'].price.data,
            deprecate = context['form'].deprecate.data,
            category_id = context['form'].category.data,
            location_id = context['form'].location.data,
            description = context['form'].description.data,
            phone = context['form'].phone.data,
            qq = context['form'].qq.data,
            valid = context['form'].valid.data,
        )
        db.session.add(sell)
        db.session.flush()
        images_files = request.files.getlist('images')
        if images_files[0]:
            images = []
            for index in xrange(len(images_files)):
                name = '%d_%d_%d%s' % (sell.id, index,
                    random.randint(100000, 999999),
                    os.path.splitext(images_files[index].filename)[-1])
                images_sell.save(images_files[index], name=name)
                images.append(name)
            sell.images = pickle.dumps(images)
        db.session.commit()
        flash(MSG_SELL_POST_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_sell'))
    return render_template("sell/post.html", **context)

@app.route('/buy/')
def buy():
    """docstring for buy"""
    context = {
        'categories': lib.get_categories(status=0),
    }
    context['buys_floors'] = lib.get_buys_floors(
        context['categories'], limit=4, status=0)
    return render_template("buy/index.html", **context)

@app.route('/buy/category/<int:id>')
def buy_category_id(id):
    """docstring for buy_category_id"""
    page = int(request.args.get('page', 1))
    context = {
        'categories': lib.get_categories(status=0),
        'category': lib.get_category(id)
    }
    context['buys'] = lib.get_buys_by_category(context['category'])
    context['pagination'] = Pagination(page=page,
        total=len(context['buys']),
        record_name='buys',
    )
    return render_template("buy/category.html", **context)

@app.route('/buy/detail/<int:id>')
def buy_id(id):
    """docstring for buy_id"""
    context = {
        'buy': lib.get_buy_by_id(id),
    }
    if context['buy'] and context['buy'].status == 0:
        return render_template("buy/detail.html", **context)
    flash(MSG_BUY_INVALID, MSG_CATEGORY_DANGER)
    return redirect(url_for('index'))

@app.route('/buy/detail/edit/<int:id>')
@login_required
def buy_edit_id(id):
    """docstring for buy_edit_id"""
    context = {
        'buy': lib.get_buy_by_id(id),
    }
    # TODO(huxuan): form of buy_edit_id
    return render_template("buy/detail_edit.html", **context)

@app.route('/buy/detail/post', methods=('GET', 'POST'))
@login_required
def buy_post():
    """docstring for buy_post"""
    context = {
        'form': forms.BuyForm(),
    }
    if context['form'].validate_on_submit():
        buy = lib.create_buy(
            user_id=g.user.id,
            title=context['form'].title.data,
            price_low=context['form'].price_low.data,
            price_high=context['form'].price_high.data,
            category_id=context['form'].category.data,
            location_id=context['form'].location.data,
            description=context['form'].description.data,
            phone=context['form'].phone.data,
            qq=context['form'].qq.data,
            valid=context['form'].valid.data,
        )
        db.session.add(buy)
        db.session.commit()
        flash(MSG_BUY_POST_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_buy'))
    return render_template("buy/post.html", **context)

@app.route('/search')
def search():
    """docstring for search"""
    q = request.args.get('q')
    page = int(request.args.get('page', 1))
    category_id = int(request.args.get('category_id', 0))
    location_id = int(request.args.get('location_id', 0))
    type_id = int(request.args.get('type_id', 0))
    context = {}
    if type_id != 2: # not only buy
        context['sells'] = lib.get_sells_q_cid_lid(
            q, category_id, location_id)
        context['sells_pagination'] = Pagination(page=page,
            total=len(context['sells']),
            record_name='sells',
        )
    if type_id != 1: # not only sell
        context['buys'] = lib.get_buys_q_cid_lid(
            q, category_id, location_id)
        context['buys_pagination'] = Pagination(page=page,
            total=len(context['buys']),
            record_name='buys',
        )
    return render_template("search.html", **context)
