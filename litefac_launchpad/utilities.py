# -*- coding: utf-8 -*-
from litefac_launchpad.basemain import db


def do_commit(*objs):
    db.session.add_all(objs)
    db.session.commit()
    return objs[0] if len(objs) == 1 else objs
