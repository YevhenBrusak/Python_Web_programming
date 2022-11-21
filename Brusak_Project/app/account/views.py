from flask import render_template, request, redirect, session, url_for, flash 
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

from .. import db
from .models import User
from .forms import RegistrationForm, LoginForm
from . import account_bp

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@account_bp.route('/register', methods=['GET','POST'])
def register() :
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()           
            flash(f'Account created for {form.username.data}! ', category='success')
            return redirect(url_for('account.login'))
        except:
            db.session.flush()
            db.session.rollback()
    return render_template('register.html', form=form)

@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home.home"))
        else:
            flash('Login unsuccessful. Please check email and password ', category='warning')    
    return render_template('login.html', form=form)
               
@account_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home.home'))

@account_bp.route('/account')
@login_required
def account():
    return render_template('account.html')

@account_bp.route('/users')
def users():
    all_users = User.query.all()
    count_users = User.query.count()
    return render_template('users.html', all_users=all_users, count=count_users)