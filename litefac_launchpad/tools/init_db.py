#! /usr/bin/env python
# -*- coding: utf-8 -*-
from litefac_launchpad.basemain import db

__import__('litefac_launchpad.models')  # 必须要import models, 否则不会建立表
db.create_all()
