#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: run.py
Author: huxuan
Email: i(at)huxuan.org
Description: run script for app
"""

from app import app
app.debug = True
app.run(host="0.0.0.0")
