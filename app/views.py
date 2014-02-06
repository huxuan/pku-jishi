#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: views for app
"""

from app import app

@app.route('/helloworld')
def helloworld():
    """docstring for helloworld"""
    return "Hello, World!"
