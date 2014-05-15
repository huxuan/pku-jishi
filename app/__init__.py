#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan < i(at)huxuan.org >
Description: init script for app
"""

from flask import Flask
from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet
from flask.ext.uploads import IMAGES
from flask.ext.uploads import configure_uploads
from flask.ext.mail import Mail
from flask.ext.images import Images
from flask.ext.mobility import Mobility
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'pkujishi_secret_key'

db = SQLAlchemy(app)
mail = Mail(app)
Mobility(app)

login_manager = LoginManager()
login_manager.init_app(app)

images_avatar = UploadSet('avatar', IMAGES)
images_sell = UploadSet('sell', IMAGES)
configure_uploads(app, (images_avatar, images_sell))

app.secret_key = 'monkey'
images = Images(app)

from app import models

class MyModelView(ModelView):
    """docstring for MyModelView"""
    def is_accessible(self):
        return g.user.id <= 3

    def __init__(self, model, session, **kwargs):
        super(MyModelView, self).__init__(model, session, **kwargs)

admin = Admin(app, name='PKUjishi Admin')
admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Category, db.session))
admin.add_view(MyModelView(models.Location, db.session))
admin.add_view(MyModelView(models.Sell, db.session))
admin.add_view(MyModelView(models.Buy, db.session))

from app import views
