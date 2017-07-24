#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField as WtStringFireld, SubmitField
from wtforms.validators import DataRequired
from mongoengine import *

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# 连接MongoDB
connect('zhouDB', host='192.168.56.102', username='zhou', password='z')


class Role(Document):
    name = StringField(max_length=64, required=True, unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Document):
    username = StringField(max_length=64, required=True, unique=True)
    # 文档引用
    role = ReferenceField(Role)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    admin = Role(name='admin').save()
    zhou = User(username='zhou').save()

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for("index"))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(FlaskForm):
    name = WtStringFireld('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run()
