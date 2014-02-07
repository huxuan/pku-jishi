#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

from flask import render_template
from app import app

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"

@app.route('/')
def index():
    """docstring for index"""
    return render_template("index.html",
        )

@app.route('/notes')
def notes():
    """docstring for notes"""
    return render_template("notes.html",
        )

@app.route('/user/login')
def user_login():
    """docstring for user_login"""
    return render_template("user/login.html",
        )

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

@app.route('/sell/category/<id>')
def sell_category_id():
    """docstring for sell_category_id"""
    return render_template("sell/category.html",
        )

@app.route('/sell/<id>')
def sell_id():
    """docstring for sell_id"""
    return render_template("sell/detail.html",
        )

@app.route('/sell/post')
def sell_post():
    """docstring for sell_post"""
    return render_template("sell/post.html",
        )

@app.route('/buy/category/<id>')
def buy_category_id():
    """docstring for buy_category_id"""
    return render_template("buy/category.html",
        )

@app.route('/buy/<id>')
def buy_id():
    """docstring for buy_id"""
    return render_template("buy/detail.html",
        )

@app.route('/buy/post')
def buy_post():
    """docstring for buy_post"""
    return render_template("buy/post.html",
        )

@app.route('/search/<q>')
def search():
    """docstring for search"""
    return render_template("search.html",
        )
