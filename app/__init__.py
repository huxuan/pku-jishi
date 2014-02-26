#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan < i(at)huxuan.org >
Description: init script for app
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet
from flask.ext.uploads import IMAGES
from flask.ext.uploads import configure_uploads
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

images_avatar = UploadSet('avatar', IMAGES)
images_sell = UploadSet('sell', IMAGES)
configure_uploads(app, (images_avatar, images_sell))

from app import views
from app import models
