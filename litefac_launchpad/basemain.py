#!/usr/bin/env python
from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("litefac_launchpad.default_settings")


@app.route('/')
def index():
    return 'hello, world'
