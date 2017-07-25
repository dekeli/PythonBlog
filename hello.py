#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import wtforms as wt
import mongoengine as db

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# 连接MongoDB
db.connect('zhouDB', host='192.168.56.102', username='zhou', password='z')


class Role(db.Document):
    name = db.StringField(max_length=64, required=True, unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Document):
    username = db.StringField(max_length=64, required=True, unique=True)
    # 文档引用
    role = db.ReferenceField(Role)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.objects(username=form.name.data)
        if len(user) is 0:
            User(username=form.name.data).save()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = None
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           know=session.get('known', False))


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
    name = wt.StringField('What is your name?', validators=[wt.validators.DataRequired()])
    submit = wt.SubmitField('Submit')


if __name__ == '__main__':
    manager.run()
