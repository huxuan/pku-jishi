#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lib.py
Author: huxuan
Email: i(at)huxuan.org
Description: lib used in app
"""

import datetime
import hashlib
import random

from app import db
from app import models

def create_user(email, name, password):
    """docstring for create_user"""
    user = models.User(
        email = email,
        name = name,
        password = hashlib.md5(password).hexdigest(),
        confirm = random.randint(100000, 999999),
        avatar = '',
        phone = '',
        qq = '',
        create_time = datetime.datetime.now(),
        status = 1,
    )
    db.session.add(user)
    db.session.commit()
