#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_drop.py
Author: huxuan
Email: i(at)huxuan.org
Description: script to drop database for initialization
"""

print 'Please input "PKU" to confirm you know what you are doing'
confirm = raw_input()

if confirm == 'PKU':
    from app import db
    db.drop_all()
