#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import urllib

from flask import Flask, render_template, request, jsonify
from flask.ext.wtf import Form, CsrfProtect
from wtforms import TextField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Regexp, Email
from pyquery import pyquery

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("litefac_launchpad.default_settings")
CsrfProtect(app)


@app.route('/')
def index():
    return render_template('index.html', demo_url=app.config['DEMO_URL'],
                           client_download_url=
                           app.config['CLIENT_DOWNLOAD_URL'])


@app.route('/application', methods=['GET', 'POST'])
def application():

    class _Form(Form):

        contact = TextField(u'联系方式',
                            validators=[
                                Regexp('1\d{10}|\d+-\d+', flags=0,
                                       message=u'手机号或者座机均可, 座机请加区号，用"-"分隔, 例如0571-12345667')
                            ])
        company_name = TextField(u'公司名称', validators=[DataRequired(message=u'请填写公司名称')])
        email = TextField(u'电子邮箱')
        tob = BooleanField(u'tob')


        def validate_email(self, field):
            if field.data.strip():
                v = Email(message=u'请填写合法的邮箱地址')
                v(self, field)

        def validate_tob(self, field):
            if field.data:
                raise ValidationError("")

    errors = {}
    form = None
    if request.method == 'POST':
        form = _Form()
        if form.validate_on_submit():
            # create
            return ""

        errors = form.errors

    return render_template('application.html', form=form or _Form(), errors=errors)

@app.route('/applications', methods=['GET', 'POST'])
def applications_view():
    applications = []
    return render_template('application_list.html', applications=applications)

@app.route('/locale')
def locale():
    contact = request.args['contact']

    if contact.startswith('1') and len(contact) == 11:
        ud = urllib.urlopen('http://api.showji.com/Locating/www.showji.co.m.aspx?m=%s&output=json' % contact)
        ret = ud.read()
    else:
        district_code = contact[:4]
        ud = urllib.urlopen('http://quhao.51240.com/%s__quhao/' % district_code)
        d = pyquery.PyQuery(ud.read())
        ret = d('table tr table tr:last-child td:last-child').text()
        d = dict(zip(('Province', 'City'), ret.split()))
        ret = jsonify(d)
    return ret
