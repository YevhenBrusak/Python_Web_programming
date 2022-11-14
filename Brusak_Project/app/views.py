# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, session, url_for, flash 
from app import app, db
from app.models import Contact, User
from app.forms import Myform, RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import os
from loguru import logger
import datetime as dt

logger.add("my.log")

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/portfolio')
def portfolio():
    return redirect(url_for('home'))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html',)


@app.route('/')
def home():  
    return render_template('index.html',name='Yevhen Brusak')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_to_db(form)
        logger.info(f"{form.name.data} {form.email.data} {form.phone.data} {form.subject.data} {form.message.data}")
        flash("Data sent successfully: " + session.get('username') + ' ' + session.get('email'), category = 'success')
        return redirect(url_for("contact"))

    elif request.method == 'POST':
        flash("POST validation failed", category = 'warning')

    if(session.get('username') == None):
        return render_template('contact.html', form=form, username="Guest")
    
    form.name.data = session.get('username')
    form.email.data = session.get('email')
    return render_template('contact.html', form=form, username=session.get('username'))

@app.route('/register', methods=['GET','POST'])
def register() :
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(url_for('login'))
        except:
            db.session.flush()
            db.session.rollback()
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash('Login unsuccessful. Please check email and password ', category='warning')    
    return render_template('login.html', form=form)
               
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/delete_session')
def delete_session():
    session.pop('username', default=None)
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'

@app.route('/database')
def database() :
    contacts = Contact.query.all()
    return render_template('database.html', contacts=contacts)

@app.route('/users')
def users():
    all_users = User.query.all()
    count_users = User.query.count()
    return render_template('users.html', all_users=all_users, count=count_users)

@app.route('/database/delete/<id>')
def delete_by_id(id):
    data = Contact.query.get(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except :
        db.session.flush()
        db.session.rollback()   
    return redirect(url_for("database"))

@app.context_processor
def inject_user():
    date = dt.datetime.now()
    os_info = [os.name,os.getlogin(),os.getpid()]
    show = current_user.is_authenticated
    return dict(user_info=request.headers.get('User-Agent'),os_info=os_info,date=date, show=show)

def save_to_db(form) :
    contact = Contact(
        name = form.name.data,
        email = form.email.data,
        phone = form.phone.data,
        subject = form.subject.data,
        message = form.message.data
    )
    try:
        db.session.add(contact)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()

if __name__ == '__main__': 
    app.run(debug=True)
