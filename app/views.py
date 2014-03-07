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
from flask import Markup
from flask import jsonify
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
MSG_USER_INVALID = u'此用户无效'
MSG_SELL_INVALID = u'此售出商品无效'
MSG_SELL_POST_SUCCESS = u'售出商品发布成功！'
MSG_BUY_INVALID = u'此求购商品无效'
MSG_BUY_POST_SUCCESS = u'求购商品发布成功！'
MSG_CHANGE_PASSWD_SUCCESS = u'修改密码成功！'
MSG_FORGET_PASSWD_SUCCESS = u'忘记密码邮件发送成功！'
MSG_SELL_EDIT_SUCCESS = u'售出商品修改成功！'
MSG_SELL_EDIT_NO_PERMISSION = u'您无权修改此售出商品'
MSG_BUY_EDIT_SUCCESS = u'求购商品修改成功！'
MSG_BUY_EDIT_NO_PERMISSION = u'您无权修改此求购商品'
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

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"

@login_manager.user_loader
def load_user(id):
    """docstring for load_user"""
    return db.session.query(models.User).get(int(id))

@app.before_request
def before_request():
    """docstring for before_request"""
    g.user = current_user
    g.user_count = lib.get_user_count()
    g.sell_count = lib.get_sell_count()
    g.buy_count = lib.get_buy_count()
    g.categories = lib.get_categories(status=0)
    g.locations = lib.get_locations(status=0)
    g.status = lib.STATUS

@app.route('/')
def index():
    """docstring for index"""
    context={
        'sells_free': lib.get_sells(price=0, limit=4, status=0),
    }
    context['sells_floors'] = lib.get_sells_floors(
        g.categories, limit=4, status=0)
    return render_template("index.html", **context)

@app.route('/join')
def join():
    """docstring for join"""
    context={
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
        email = context['form'].email.data
        user = db.session.query(models.User).filter_by(email=email).first()
        remember = context['form'].remember.data
        login_user(user, remember=remember)
        #flash(MSG_LOGIN_SUCCESS, MSG_CATEGORY_SUCCESS)
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
    context = {
        'form': forms.EmailCaptchaForm(),
    }
    if context['form'].validate_on_submit():
        email = context['form'].email.data
        user = db.session.query(models.User).filter_by(email=email).first()
        token = lib.create_token(user)
        db.session.add(token)
        db.session.commit()
        url = url_for('user_activation', token=token, _external=True)
        token = lib.activation_token_encode(user.id, token.confirm)
        lib.send_activation_mail(user, url)
        flash(MSG_RESEND_CONFIRM_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_index'))
    return render_template("user/resend_confirm_mail.html", **context)

@app.route('/user/activation/<token>')
def user_activation(token):
    """docstring for user_activation"""
    user_id, confirm = lib.activation_token_decode(token)
    if user_id:
        user = db.session.query(models.User).get(user_id)
        if user and user.token.confirm == confirm:
            user.status = 0
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
        user = db.session.query(models.User).filter_by(email=email).first()
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
        user = db.session.query(models.User).get(user_id)
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
def user_sell():
    """docstring for user_sell"""
    context = {
        'sells': lib.get_sells(user_id=g.user.id, status=0)
    }
    return render_template("user/sell.html", **context)

@app.route('/user/buy')
@login_required
def user_buy():
    """docstring for user_buy"""
    context = {
        'buys': lib.get_buys(user_id=g.user.id, status=0),
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
    context = {}
    context['user'] = db.session.query(models.User).get(id)
    if not context['user'] or context['user'].status > 1:
        flash(MSG_USER_INVALID, MSG_CATEGORY_DANGER)
        return redirect(url_for('index'))
    context['sells'] = lib.get_sells(user_id=id)
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

@app.route('/sell/')
@app.route('/sell/index')
def sell_index():
    """docstring for sell_index"""
    page = int(request.args.get('page', 1))
    status = int(request.args.get('status', 0))
    location_id = int(request.args.get('location_id', 0))
    category_id = int(request.args.get('category_id', 0))
    context = {
        'sells': lib.get_sells(status=status, location_id=location_id,
            category_id=category_id)
    }
    context['pagination'] = Pagination(page=page,
        total=len(context['sells']),
        record_name='sells',
        css_framework='foundation',
    )
    return render_template("sell/index.html", **context)

@app.route('/sell/update')
def sell_update():
    """docstring for sell_update"""
    res = {}
    id = int(request.args.get('id', 0))
    status = int(request.args.get('status', 0))
    sell = lib.get_sell_by_id(id)
    if sell.id != g.user.id:
        res['error'] = MSG_SELL_PERMISSION_INVALID
    if not id or not sell:
        res['error'] = MSG_SELL_ID_INVALID
    if not status:
        res['error'] = MSG_SELL_STATUS_INVALID
    sell.status = status
    return jsonify(**res)

@app.route('/sell/free')
def sell_free():
    """docstring for sell_free"""
    page = int(request.args.get('page', 1))
    context = {
        'sells': lib.get_sells(price=0, limit=1000, status=0)
    }
    context['pagination'] = Pagination(page=page,
        total=len(context['sells']),
        record_name='sells',
        css_framework='foundation'
    )
    return render_template("sell/free.html", **context)

@app.route('/sell/category/<int:id>')
def sell_category_id(id):
    """docstring for sell_category_id"""
    page = int(request.args.get('page', 1))
    context = {
        'category': lib.get_category(id)
    }
    context['sells'] = lib.get_sells(category_id=id)
    context['pagination'] = Pagination(page=page,
        total=len(context['sells']),
        record_name='sells',
        css_framework='foundation'
    )
    return render_template("sell/category.html", **context)

@app.route('/sell/detail/<int:id>')
def sell_id(id):
    """docstring for sell_id"""
    context = {
        'sell': lib.get_sell_by_id(id),
    }
    context['images'] = lib.images_decode(images_sell, context['sell'].images)
    if context['sell'] and context['sell'].status <= 1:
        return render_template("sell/detail.html", **context)
    flash(MSG_SELL_INVALID, MSG_CATEGORY_DANGER)
    return redirect(url_for('index'))

@app.route('/sell/detail/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def sell_edit_id(id):
    """docstring for sell_edit_id"""
    sell = lib.get_sell_by_id(id)
    if g.user.id != sell.user_id:
        flash(MSG_SELL_EDIT_NO_PERMISSION, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_sell'))
    context = {
        'form': forms.SellForm(obj=sell),
        'images': lib.images_decode(images_sell, sell.images),
    }
    if context['form'].validate_on_submit():
        sell = lib.update_sell_from_form(sell, context['form'])
        images_files = request.files.getlist('images')
        sell.images = lib.images_encode(images_sell, sell.id, images_files)
        db.session.commit()
        flash(MSG_SELL_EDIT_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('sell_id', id=sell.id))
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
            category_id = context['form'].category_id.data,
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
def buy():
    """docstring for buy"""
    context = {
        'buys_floors': lib.get_buys_floors(
            g.categories, limit=4, status=0)
    }
    return render_template("buy/index.html", **context)

@app.route('/buy/update')
def buy_update():
    """docstring for buy_update"""
    res = {}
    id = int(request.args.get('id', 0))
    status = int(request.args.get('status', 0))
    buy = lib.get_buy_by_id(id)
    if buy.id != g.user.id:
        res['error'] = MSG_BUY_PERMISSION_INVALID
    if not id or not buy:
        res['error'] = MSG_BUY_ID_INVALID
    if not status:
        res['error'] = MSG_BUY_STATUS_INVALID
    sell.status = status
    return jsonify(**res)

@app.route('/buy/category/<int:id>')
def buy_category_id(id):
    """docstring for buy_category_id"""
    page = int(request.args.get('page', 1))
    context = {
        'category': lib.get_category(id)
    }
    context['buys'] = lib.get_buys(category_id=id)
    context['pagination'] = Pagination(page=page,
        total=len(context['buys']),
        record_name='buys',
        css_framework='foundation'
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

@app.route('/buy/detail/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def buy_edit_id(id):
    """docstring for buy_edit_id"""
    buy = lib.get_buy_by_id(id)
    if g.user.id != buy.user_id:
        flash(MSG_BUY_EDIT_NO_PERMISSION, MSG_CATEGORY_DANGER)
        return redirect(url_for('user_buy'))
    context = {
        'form': forms.BuyForm(obj=buy),
    }
    if context['form'].validate_on_submit():
        buy = lib.update_buy_from_form(buy, context['form'])
        db.session.commit()
        flash(MSG_BUY_EDIT_SUCCESS, MSG_CATEGORY_SUCCESS)
        return redirect(url_for('user_buy'))
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
            category_id=context['form'].category_id.data,
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
    category_id = int(request.args.get('category_id', 0))
    location_id = int(request.args.get('location_id', 0))
    type_id = int(request.args.get('type_id', 0))
    context = {}
    context['q'] = q
    if type_id != 2: # not only buy
        context['sells'] = lib.get_sells_q_cid_lid(
            q, category_id, location_id)
        context['sells_pagination'] = Pagination(page=page,
            total=len(context['sells']),
            record_name='sells',
            css_framework='foundation'
        )
    if type_id != 1: # not only sell
        context['buys'] = lib.get_buys_q_cid_lid(
            q, category_id, location_id)
        context['buys_pagination'] = Pagination(page=page,
            total=len(context['buys']),
            record_name='buys',
            css_framework='foundation'
        )
    return render_template("search.html", **context)
