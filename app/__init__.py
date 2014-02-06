#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan < i(at)huxuan.org >
Description: init script for app
"""

from flask import Flask

app = Flask(__name__)
from app import views
