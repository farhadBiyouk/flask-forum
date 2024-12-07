from crypt import methods

from flask import Blueprint, render_template, session, url_for, redirect, flash
from flask_login import login_user, logout_user

from .models import User, Code
from .forms import RegisterationForm, CodeVerifyForm, LoginForm
from ..extensions import db

import datetime, random

blueprint = Blueprint('users', __name__)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterationForm()
	if form.validate_on_submit():
		rand_code = random.randint(1000, 9999)
		print(rand_code)
		session['phone_number'] = form.phone_number.data
		session['code'] = rand_code
		session['username'] = form.username.data
		session['email'] = form.email.data
		code = Code(
			code=rand_code,
			phone_number=form.phone_number.data,
			expire_time=datetime.datetime.now() + datetime.timedelta(minutes=10))
		db.session.add(code)
		db.session.commit()
		return redirect(url_for('users.verify'))
	return render_template('users/register.html', form=form)


@blueprint.route('/verify', methods=['GET', 'POST'])
def verify():
	phone = session.get('phone_number')
	code = Code.query.filter_by(phone_number=phone).first()
	form = CodeVerifyForm()
	if form.validate_on_submit():
		if code.expire_time < datetime.datetime.now():
			flash('this code invali or pass time ', 'danger')
			return redirect(url_for('users.register'))
		if form.code.data != str(code.code):
			flash('this code is wrong', 'danger')
		else:
			user = User(phone_number=code.phone_number, username=session.get('username'), email=session.get('email'))
			db.session.add(user)
			db.session.commit()
			flash('you registered successfully', 'success')
			return redirect(url_for('users.login'))
	return render_template('users/verify.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(phone_number=form.phone_number.data).first()
		if user:
			rand_code = random.randint(100000, 999999)
			session['code'] = rand_code
			session['phone_number'] = form.phone_number.data
			print(rand_code)
			code = Code(
				code=rand_code,
				phone_number=form.phone_number.data,
				expire_time=datetime.datetime.now() + datetime.timedelta(minutes=10))
			db.session.add(code)
			db.session.commit()
			return redirect(url_for('users.verify_code_login'))
		else:
			flash('this user not found', 'danger')
	return render_template('users/login.html', form=form)


@blueprint.route('/verify_login', methods=['GET', 'POST'])
def verify_code_login():
	phone = session.get('phone_number')
	code = Code.query.filter_by(phone_number=phone).first()
	form = CodeVerifyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(phone_number=phone).first()
		if code.expire_time < datetime.datetime.now():
			flash('this code invali or pass time ', 'danger')
			return redirect(url_for('users.register'))
		if form.code.data != str(code.code):
			flash('this code is wrong', 'danger')
		else:
			login_user(user)
			
			flash('you logged in successfully', 'success')
			return redirect(url_for('users.profile'))
	return render_template('users/verify.html', form=form)


@blueprint.route('/profile')
def profile():
	return 'Hello profile'
