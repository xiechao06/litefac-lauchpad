# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from datetime import datetime

from litefac_launchpad.basemain import db


class Application(db.Model):

    __tablename__ = 'TB_APPLICATION'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(32), nullable=False, unique=True)
    contact = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    linkman = db.Column(db.String(32))
    create_time = db.Column(db.DateTime, default=datetime.now)
