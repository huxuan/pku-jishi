#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

import random
import string
import hashlib
import StringIO
from functools import wraps

from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import Markup
from flask import jsonify
from flask import session
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

from config import PER_PAGE

MSG_CATEGORY_SUCCESS = 'success'
MSG_CATEGORY_INFO = 'info'
MSG_CATEGORY_WARNING = 'warning'
MSG_CATEGORY_DANGER = 'danger'

MSG_LOGIN_REQUIRED = u'请登录后查看此页面'
MSG_LOGIN_SUCCESS = u'登录成功！'
MSG_ACTIVATION_REQUIRED = u'请激活后使用该功能'
MSG_USER_INVALID = u'此用户无效'
MSG_SELL_INVALID = u'此售出商品无效'
MSG_SELL_POST_SUCCESS = u'售出商品发布成功！'
MSG_BUY_INVALID = u'此求购商品无效'
MSG_BUY_POST_SUCCESS = u'求购商品发布成功！'
MSG_CHANGE_PASSWD_SUCCESS = u'修改密码成功！'
MSG_FORGET_PASSWD_SUCCESS = u'忘记密码邮件发送成功！'
MSG_SELL_EDIT_SUCCESS = u'售出商品修改成功！'
MSG_SELL_EDIT_NO_PERMISSION = u'您无权修改此售出商品'
MSG_SELL_EDIT_INVALID = u'此售出商品无效'
MSG_BUY_EDIT_SUCCESS = u'求购商品修改成功！'
MSG_BUY_EDIT_NO_PERMISSION = u'您无权修改此求购商品'
MSG_BUY_EDIT_INVALID = u'此求购商品无效'
MSG_USER_ACTIVATION_SUCCESS = u'用户激活成功！'
MSG_USER_ACTIVATION_FAIL = u'用户激活失败，您可以选择重新发送激活邮件'
MSG_RESEND_CONFIRM_SUCCESS = u'验证邮件发送成功！'
MSG_RESET_PASSWD_SUCCESS = u'重置密码成功！'
MSG_RESET_PASSWD_FAIL = u'重置密码失败'
MSG_SELL_PERMISSION_INVALID = u'您无权修改此售出商品'
MSG_SELL_ID_INVALID = u'此售出商品无效'
MSG_SELL_STATUS_INVALID = u'售出商品状态无效'
MSG_BUY_PERMISSION_INVALID = u'您无权修改此求购商品'
MSG_BUY_ID_INVALID = u'此求购商品无效'
MSG_BUY_STATUS_INVALID = u'求购商品状态无效'

login_manager.login_view = 'user_login'
login_manager.login_message = MSG_LOGIN_REQUIRED
login_manager.login_message_category = MSG_CATEGORY_DANGER

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

def activation_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user.is_anonymous() and g.user.status == 0:
            return f(*args, **kwargs)
        flash(MSG_ACTIVATION_REQUIRED, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_resend_confirm_mail'))
    return wrapper

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"

@login_manager.user_loader
def load_user(id):
    """docstring for load_user"""
    return lib.get_user_by_id(int(id))

@app.before_request
def before_request():
    """docstring for before_request"""
    g.user = current_user
    g.user_count = lib.get_user_count()
    g.sell_count = lib.get_sell_count()
    g.buy_count = lib.get_buy_count()
    g.categories = lib.get_categories()
    g.subcategories = lib.get_subcategories()
    g.locations = lib.get_locations()
    g.status = lib.STATUS

@app.route('/')
def index():
    """docstring for index"""
    if request.MOBILE:
        return redirect(url_for('m'))
    statuses = request.args.getlist('status') or [0]
    context = {
        'sells_free': lib.get_sells(price=0, page=1, per_page=4,
            statuses=statuses)[1],
    }
    context['sells_floors'] = lib.get_sells_floors(g.categories,
        statuses=statuses, page=1, per_page=4)
    return render_template("index.html", **context)

@app.route('/intro')
def intro():
    context = {
    }
    return render_template("intro.html", **context)

@app.route('/phone_intro')
def phone_intro():
    context = {
    }
    return render_template("phone_intro.html", **context)

@app.route('/m')
def m():
    """docstring for m"""
    context = {
    }
    return render_template("mobile/index.html", **context)

@app.route('/join')
def join():
    """docstring for join"""
    context = {
    }
    return render_template("join.html", **context)

@app.route('/user/login', methods=('GET', 'POST'))
def user_login():
    """docstring for user_login"""
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))
    context={
        'form': forms.LoginForm(),
    }
    if context['form'].validate_on_submit():
        email_or_name = context['form'].email_or_name.data
        if '@' in email_or_name:
            user = lib.get_user_by_email(email_or_name)
        else:
            user = lib.get_user_by_name(email_or_name)
        remember = context['form'].remember.data
        login_user(user, remember=remember)
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
        db.session.flush()
        token = lib.create_token(user)
        db.session.add(token)
        db.session.commit()
        token = lib.activation_token_encode(user.id, token.confirm)
        url = url_for('user_activation', token=token, _external=True)
        lib.send_activation_mail(user, url)
        return redirect(url_for('user_register_succ'))
    return render_template("user/register.html", **context)

@app.route('/user/register_succ')
def user_register_succ():
    """docstring for user_register_succ"""
    return render_template("user/register_succ.html")

@app.route('/user/resend_confirm_mail', methods=('GET', 'POST'))
def user_resend_confirm_mail():
    """docstring for user_resend_confirm_mail"""
    if g.user.status == 0:
        return redirect(url_for('user_index'))
    context = {
        'form': forms.EmailCaptchaForm(),
    }
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        user = lib.get_user_by_email(email)
        token = lib.create_token(user)
        db.session.add(token)
        db.session.commit()
        url = url_for('user_activation', token=token, _external=True)
        token = lib.activation_token_encode(user.id, token.confirm)
        lib.send_activation_mail(user, url)
        flash(MSG_RESEND_CONFIRM_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_register_succ'))
    return render_template("user/resend_confirm_mail.html", **context)

@app.route('/user/activation/<token>')
def user_activation(token):
    """docstring for user_activation"""
    user_id, confirm = lib.activation_token_decode(token)
    if user_id:
        user = lib.get_user_by_id(user_id)
        if user and user.token.confirm == confirm:
            user.status = 0
            db.session.commit()
            flash(MSG_USER_ACTIVATION_SUCCESS, MSG_CATEGORY_SUCCESS)
            if user == g.user:
                return redirect(url_for('user_index'))
            else:
                logout_user()
                return redirect(url_for('user_login'))
    flash(MSG_USER_ACTIVATION_FAIL, MSG_CATEGORY_DANGER)
    return redirect(url_for('user_resend_confirm_mail'))

@app.route('/user/forget_password', methods=('GET', 'POST'))
def user_forget_password():
    """docstring for user_forget_password"""
    context = {
        'form': forms.EmailCaptchaForm(),
    }
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        user = lib.get_user_by_email(email)
        token = lib.create_token(user)
        db.session.add(token)
        db.session.commit()
        token = lib.password_token_encode(user.id, token.confirm)
        url = url_for('user_reset_password', token=token, _external=True)
        lib.send_password_mail(user, url)
        flash(MSG_FORGET_PASSWD_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('index'))
    return render_template("user/forget_password.html", **context)

@app.route('/user/reset_password/<token>', methods=('GET', 'POST'))
def user_reset_password(token):
    """docstring for user_reset_password"""
    user_id, confirm = lib.password_token_decode(token)
    flag = False
    if user_id:
        user = lib.get_user_by_id(user_id)
        if user and user.token.confirm == confirm:
            flag = True
    if not flag:
        flash(MSG_RESET_PASSWD_FAIL, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_forget_password'))
    context = {
        'form': forms.ResetPasswordForm(),
    }
    if context['form'].validate_on_submit():
        lib.set_password(user, context['form'].password.data)
        db.session.commit()
        flash(MSG_RESET_PASSWD_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_info'))
    return render_template("user/reset_password.html", **context)

@app.route('/user/change_password', methods=('GET', 'POST'))
@login_required
def user_change_password():
    """docstring for user_change_password"""
    context = {
        'form': forms.ChangePasswordForm(),
    }
    if context['form'].validate_on_submit():
        lib.set_password(g.user, context['form'].new_password.data)
        db.session.commit()
        flash(MSG_CHANGE_PASSWD_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_info'))
    return render_template("user/change_password.html", **context)

@app.route('/user/sell')
@login_required
@activation_required
def user_sell():
    """docstring for user_sell"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0,1,2,3]
    context = {}
    total, context['sells'] = lib.get_sells(user_id=g.user.id,
        statuses=statuses, page=page, per_page=PER_PAGE)
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='sells',
        per_page=PER_PAGE,
        css_framework='foundation',
    )
    return render_template("user/sell.html", **context)

@app.route('/user/buy')
@login_required
@activation_required
def user_buy():
    """docstring for user_buy"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0,1,2]
    context = {}
    total, context['buys'] = lib.get_buys(user_id=g.user.id,
        statuses=statuses, page=page, per_page=PER_PAGE)
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='buys',
        per_page=PER_PAGE,
        css_framework='foundation',
    )
    return render_template("user/buy.html", **context)

@app.route('/user/index')
@login_required
@activation_required
def user_index():
    """docstring for user_index"""
    return redirect(url_for('user_id',id=g.user.id))

@app.route('/user/<int:id>')
def user_id(id):
    """docstring for user_id"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0]
    context = {}
    context['user'] = lib.get_user_by_id(id)
    if not context['user'] or context['user'].status > 1:
        flash(MSG_USER_INVALID, MSG_CATEGORY_DANGER)
        return redirect(url_for('index'))
    total, context['sells'] = lib.get_sells(user_id=id, statuses=statuses,
        page=page, per_page=PER_PAGE)
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='sells',
        per_page=PER_PAGE,
        css_framework='foundation',
    )
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

@app.route('/user/info/edit', methods=('GET', 'POST'))
@login_required
def user_info_edit():
    """docstring for user_info_edit"""
    context = {
        'form': forms.UserEditForm(obj=g.user),
    }
    if context['form'].validate_on_submit():
        g.user.phone = context['form'].phone.data
        g.user.qq = context['form'].qq.data
        db.session.commit()
        return redirect(url_for('user_info'))
    return render_template("user/info_edit.html", **context)

@app.route('/sell/')
@app.route('/sell/index')
def sell_index():
    """docstring for sell_index"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0]
    context = {
        'location_id': int(request.args.get('location_id', 0)),
        'category_id': int(request.args.get('category_id', 0))
    }
    total, context['sells'] = lib.get_sells(statuses=statuses,
        location_id=context['location_id'],
        category_id=context['category_id'],
        page=page, per_page=PER_PAGE)
    context['total'] = total
    context['page'] = page
    context['per_page'] = PER_PAGE
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='sells',
        per_page=PER_PAGE,
        css_framework='foundation',
    )
    return render_template("sell/index.html", **context)

@app.route('/sell/update')
@login_required
@activation_required
def sell_update():
    """docstring for sell_update"""
    res = {}
    id = int(request.args.get('id', 0))
    status = int(request.args.get('status', 0))
    sell = lib.get_sell_by_id(id)
    if sell.user.id != g.user.id:
        res['error'] = MSG_SELL_PERMISSION_INVALID
    if not id or not sell:
        res['error'] = MSG_SELL_ID_INVALID
    if status > 4:
        res['error'] = MSG_SELL_STATUS_INVALID
    res['status'] = res.get('error') and 'ERROR' or 'OK'
    sell.status = status
    db.session.commit()
    return jsonify(**res)

@app.route('/sell/free')
def sell_free():
    """docstring for sell_free"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0]
    context = {
        'location_id': int(request.args.get('location_id', 0)),
        'category_id': int(request.args.get('category_id', 0)),
    }
    total, context['sells'] = lib.get_sells(price=0, statuses=statuses,
        location_id=context['location_id'],
        category_id=context['category_id'],
        page=page, per_page=PER_PAGE)
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='sells',
        per_page=PER_PAGE,
        css_framework='foundation'
    )
    return render_template("sell/free.html", **context)

@app.route('/sell/detail/<int:id>')
def sell_id(id):
    """docstring for sell_id"""
    context = {
        'sell': lib.get_sell_by_id(id),
    }
    context['images'] = lib.images_decode(images_sell, context['sell'].images)
    context['sell'].phone = lib.number_encode(context['sell'].phone)
    context['sell'].qq = lib.number_encode(context['sell'].qq)
    if context['sell'] and context['sell'].status < 5:
        return render_template("sell/detail.html", **context)
    flash(MSG_SELL_INVALID, MSG_CATEGORY_DANGER)
    return redirect(url_for('index'))

@app.route('/sell/detail/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@activation_required
def sell_edit_id(id):
    """docstring for sell_edit_id"""
    sell = lib.get_sell_by_id(id)
    if g.user.id != sell.user_id:
        flash(MSG_SELL_EDIT_NO_PERMISSION, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_sell'))
    if sell.status > 4:
        flash(MSG_SELL_EDIT_INVALID, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_sell'))
    context = {
        'form': forms.SellForm(obj=sell),
        'images': lib.images_decode(images_sell, sell.images),
    }
    category_id = sell.category_id
    if category_id > len(g.categories):
        subcategory_id = category_id
        context['form'].subcategory_id.data = subcategory_id
        subcategory = lib.get_category_by_id(subcategory_id)
        category_id = subcategory.parent_id
        context['form'].category_id.data = category_id
    category_id = context['form'].category_id.data
    if category_id > 0 and category_id <= len(g.categories):
        context['form'].subcategory_id.choices = [(x['id'], x['name'])
            for x in g.subcategories[category_id - 1]]
    if context['form'].validate_on_submit():
        sell = lib.update_sell_from_form(sell, context['form'])
        images_files = request.files.getlist('images')
        images_temp, thumbnails_temp = lib.images_encode(
            images_sell, sell.id, images_files)
        if thumbnails_temp:
            sell.images = images_temp
            sell.thumbnails = thumbnails_temp
        db.session.commit()
        flash(MSG_SELL_EDIT_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('sell_id', id=sell.id))
    return render_template("sell/detail_edit.html", **context)

@app.route('/sell/detail/post', methods=('GET', 'POST'))
@login_required
@activation_required
def sell_post():
    """docstring for sell_post"""
    context = {
        'form': forms.SellForm(obj=g.user),
    }
    category_id = context['form'].category_id.data
    if category_id > 0 and category_id <= len(g.categories):
        context['form'].subcategory_id.choices = [(x['id'], x['name'])
            for x in g.subcategories[category_id - 1]]
    if context['form'].validate_on_submit():
        sell = lib.create_sell(
            user_id = g.user.id,
            title = context['form'].title.data,
            price = context['form'].price.data,
            deprecate = context['form'].deprecate.data,
            category_id = context['form'].category_id.data,
            subcategory_id = context['form'].subcategory_id.data,
            location_id = context['form'].location_id.data,
            description = context['form'].description.data,
            phone = context['form'].phone.data,
            qq = context['form'].qq.data,
            valid = context['form'].valid.data,
        )
        db.session.add(sell)
        db.session.flush()
        images_files = request.files.getlist('images')
        sell.images, sell.thumbnails = lib.images_encode(
            images_sell, sell.id, images_files)
        db.session.commit()
        flash(MSG_SELL_POST_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_sell'))
    return render_template("sell/post.html", **context)

@app.route('/buy/')
@app.route('/buy/index')
def buy_index():
    """docstring for buy_index"""
    page = int(request.args.get('page', 1))
    statuses = request.args.getlist('status') or [0]
    context = {
        'location_id': int(request.args.get('location_id', 0)),
        'category_id': int(request.args.get('category_id', 0)),
    }
    total, context['buys'] = lib.get_buys(statuses=statuses,
            location_id=context['location_id'],
            category_id=context['category_id'],
            page=page, per_page=PER_PAGE)
    for buy in context['buys']:
        buy.phone = lib.number_encode(buy.phone)
        buy.qq = lib.number_encode(buy.qq)
    context['pagination'] = Pagination(page=page,
        total=total,
        record_name='buys',
        per_page=PER_PAGE,
        css_framework='foundation',
    )
    return render_template("buy/index.html", **context)

@app.route('/buy/update')
@login_required
@activation_required
def buy_update():
    """docstring for buy_update"""
    res = {}
    id = int(request.args.get('id', 0))
    status = int(request.args.get('status', 0))
    buy = lib.get_buy_by_id(id)
    if buy.user.id != g.user.id:
        res['error'] = MSG_BUY_PERMISSION_INVALID
    if not id or not buy:
        res['error'] = MSG_BUY_ID_INVALID
    if status > 3:
        res['error'] = MSG_BUY_STATUS_INVALID
    res['status'] = res.get('error') and 'ERROR' or 'OK'
    buy.status = status
    db.session.commit()
    return jsonify(**res)

@app.route('/buy/detail/<int:id>')
@login_required
@activation_required
def buy_id(id):
    """docstring for buy_id"""
    context = {
        'buy': lib.get_buy_by_id(id),
    }
    context['buy'].phone = lib.number_encode(context['buy'].phone)
    context['buy'].qq = lib.number_encode(context['buy'].qq)
    if context['buy'] and context['buy'].status < 4:
        return render_template("buy/detail.html", **context)
    flash(MSG_BUY_INVALID, MSG_CATEGORY_DANGER)
    return redirect(url_for('index'))

@app.route('/buy/detail/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@activation_required
def buy_edit_id(id):
    """docstring for buy_edit_id"""
    buy = lib.get_buy_by_id(id)
    if g.user.id != buy.user_id:
        flash(MSG_BUY_EDIT_NO_PERMISSION, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_buy'))
    if buy.status > 3:
        flash(MSG_BUY_EDIT_INVALID, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_buy'))
    context = {
        'form': forms.BuyForm(obj=buy),
    }
    category_id = sell.category_id
    if category_id > len(g.categories):
        subcategory_id = category_id
        context['form'].subcategory_id.data = subcategory_id
        subcategory = lib.get_category_by_id(subcategory_id)
        category_id = subcategory.parent_id
        context['form'].category_id.data = category_id
    category_id = context['form'].category_id.data
    if category_id > 0 and category_id <= len(g.categories):
        context['form'].subcategory_id.choices = [(x['id'], x['name'])
            for x in g.subcategories[category_id - 1]]
    if context['form'].validate_on_submit():
        buy = lib.update_buy_from_form(buy, context['form'])
        db.session.commit()
        flash(MSG_BUY_EDIT_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_buy'))
    return render_template("buy/detail_edit.html", **context)

@app.route('/buy/detail/post', methods=('GET', 'POST'))
@login_required
@activation_required
def buy_post():
    """docstring for buy_post"""
    context = {
        'form': forms.BuyForm(obj=g.user),
    }
    category_id = context['form'].category_id.data
    if category_id > 0 and category_id <= len(g.categories):
        context['form'].subcategory_id.choices = [(x['id'], x['name'])
            for x in g.subcategories[category_id - 1]]
    if context['form'].validate_on_submit():
        buy = lib.create_buy(
            user_id=g.user.id,
            title=context['form'].title.data,
            price_low=context['form'].price_low.data,
            price_high=context['form'].price_high.data,
            category_id=context['form'].category_id.data,
            subcategory_id=context['form'].subcategory_id.data,
            location_id=context['form'].location_id.data,
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
    statuses = request.args.getlist('status') or [0]
    category_id = int(request.args.get('category_id', 0))
    location_id = int(request.args.get('location_id', 0))
    types = request.args.getlist('type') or ['sell', 'buy']
    context = {}
    context['q'] = q
    if 'sell' in types:
        total, context['sells'] = lib.get_sells_q_cid_lid(
            q, category_id, location_id, statuses=statuses,
            page=page, per_page=PER_PAGE)
        context['sells_pagination'] = Pagination(page=page,
            total=total,
            record_name='sells',
            per_page=PER_PAGE,
            css_framework='foundation',
        )
    if 'buy' in types:
        total, context['buys'] = lib.get_buys_q_cid_lid(
            q, category_id, location_id, statuses=statuses,
            page=page, per_page=PER_PAGE)
        context['buys_pagination'] = Pagination(page=page,
            total=total,
            record_name='buys',
            per_page=PER_PAGE,
            css_framework='foundation'
        )
    return render_template("search.html", **context)

@app.route('/captcha')
def captcha():
    """docstring for captcha"""
    code = ''.join(random.sample(string.uppercase + string.digits, 4))
    session['captcha'] = hashlib.md5(code.lower()).hexdigest()
    image = lib.generate_captcha(code)
    buf = StringIO.StringIO()
    image.save(buf, 'JPEG', quality=75)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response
