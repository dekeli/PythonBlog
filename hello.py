#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import wtforms as wt

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zhou:z@192.168.56.102:3306/python_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.CHAR(36), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.CHAR(36), primary_key=True)
    username = db.Column(db.CHAR(36), unique=True)
    role_id = db.Column(db.CHAR(36), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.objects(username=form.name.data)
    #     if len(user) is 0:
    #         User(username=form.name.data).save()
    #         session['known'] = False
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     form.name.data = None
    #     return redirect(url_for('index'))
    # return render_template('index.html',
    #                        form=form, name=session.get('name'),
    #                        know=session.get('known', False))
    return render_template('index.html')


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
    name = wt.StringField('What is your name?', validators=[
        wt.validators.DataRequired()])
    submit = wt.SubmitField('Submit')


if __name__ == '__main__':
    manager.run()
