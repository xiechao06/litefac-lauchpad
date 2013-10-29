#!/usr/bin/env python
from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("litefac_launchpad.default_settings")


@app.route('/')
def index():
    return render_template('index.html', demo_url=app.config['DEMO_URL'],
                           client_download_url=
                           app.config['CLIENT_DOWNLOAD_URL'])
