#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: apis.py
Author: huxuan
Email: i(at)huxuan.org
Description: apis for app
"""

from flask import jsonify
from app import app

def api(func):
    def api_and_call(*args, **kwargs):
        return jsonify(func(*args, **kwargs))
    return api_and_call

@app.route('/api/helloworld')
@api
def api_helloworld():
    """docstring for api_helloworld"""
    return {'Hello': 'World'}
