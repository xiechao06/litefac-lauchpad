#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import re
import urllib

from flask import Flask, render_template, request, jsonify, g
from flask.ext.wtf import Form, CsrfProtect
from wtforms import TextField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Regexp, Email
from pyquery import pyquery
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


from litefac_launchpad.constants import PAGE_SIZE

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("litefac_launchpad.default_settings")
if os.path.exists('config.py'):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
CsrfProtect(app)
db = SQLAlchemy(app)

from litefac_launchpad.utilities import do_commit, request_from_mobile
from litefac_launchpad import models


@app.before_request
def test_request_type():
    g.request_from_mobile = request_from_mobile()


@app.route('/')
def index():
    return render_template('index.html', demo_url=app.config['DEMO_URL'],
                           client_download_url=
                           app.config['CLIENT_DOWNLOAD_URL'])


class ApplicationViewForm(Form):

    contact = TextField(u'联系电话',
                        validators=[
                            Regexp('1\d{10}|\d+-\d+', flags=0,
                                   message=u'手机号或者座机均可, 座机请加'
                                   u'区号，用"-"分隔, 例如0571-12345667')
                        ])
    company_name = TextField(u'公司名称',
                             validators=[
                                 DataRequired(u'必填')])
    linkman = TextField(u'联系人',
                        validators=[
                            DataRequired(u'必填')])
    email = TextField(u'电子邮箱')
    tob = BooleanField(u'tob')

    def validate_email(self, field):
        if field.data.strip():
            v = Email(message=u'请填写合法的邮箱地址')
            v(self, field)

    def validate_tob(self, field):
        if field.data:
            raise ValidationError("")


@app.route('/application', methods=['GET', 'POST'])
def application_view():
    errors = {}
    form = None
    total_application_cnt = models.Application.query.count()
    if request.method == 'POST':
        form = ApplicationViewForm()
        if form.validate_on_submit():
            try:
                application = do_commit(models.Application(
                    company_name=form.company_name.data,
                    contact=form.contact.data,
                    email=form.email.data,
                    linkman=form.linkman.data))
                return render_template('message.html', application=application,
                                       total_application_cnt=
                                       total_application_cnt)
            except IntegrityError:
                errors = {"company_name": [u'该公司已经注册过了']}
                db.session.rollback()
        else:
            errors = form.errors

    return render_template('application.html',
                           form=form or ApplicationViewForm(),
                           errors=errors,
                           total_application_cnt=total_application_cnt)


def _fuzz_contact(contact):
    p = re.compile('(\d+)-(\d+)')
    m = p.match(contact)
    if m:
        return m.group(1) + '-' + '*' * (len(m.group(2)) - 4) + m.group(2)[-4:]
    return contact[:3] + '****' + contact[-4:]


@app.route('/applications', methods=['GET', 'POST'])
def applications_view():
    page = int(request.args.get('page', 0))
    q = models.Application.query
    total_application_cnt = q.count()
    total_page_cnt = ((total_application_cnt - 1) / PAGE_SIZE) + 1
    applications = q.order_by(models.Application.create_time.desc()).offset(
        page * PAGE_SIZE).limit(PAGE_SIZE).all()
    applications = [dict(contact=_fuzz_contact(a.contact),
                         company_name=a.company_name[:3] +
                         '*' * (len(a.company_name) - 3),
                         linkman=a.linkman,
                         create_time=a.create_time.strftime('%Y-%d-%m %H:%S'))
                    for a in applications]
    return render_template('application_list.html', applications=applications,
                           page=page, total_page_cnt=total_page_cnt,
                           total_application_cnt=total_application_cnt)


@app.route('/locale')
def locale():
    contact = request.args['contact']

    if contact.startswith('1') and len(contact) == 11:
        ud = urllib.urlopen('http://api.showji.com/Locating/www.showji.co.m.a'
                            'spx?m=%s&output=json' % contact)
        ret = ud.read()
    else:
        district_code = contact[:4]
        ud = urllib.urlopen('http://quhao.51240.com/%s__quhao/' %
                            district_code)
        d = pyquery.PyQuery(ud.read())
        ret = d('table tr table tr:last-child td:last-child').text()
        d = dict(zip(('Province', 'City'), ret.split()))
        ret = jsonify(d)
    return ret


@app.route('/questions')
def questions():
    return render_template('questions.html')
