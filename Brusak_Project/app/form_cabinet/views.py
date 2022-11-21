from flask import render_template, request, redirect, session, url_for, flash 
from loguru import logger
from .. import db
from .models import Contact
from .forms import Myform

from . import cabinet_bp

logger.add("my.log")

@cabinet_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_to_db(form)
        logger.info(f"{form.name.data} {form.email.data} {form.phone.data} {form.subject.data} {form.message.data}")
        flash("Data sent successfully: " + session.get('username') + ' ' + session.get('email'), category = 'success')
        return redirect(url_for("cabinet.contact"))

    elif request.method == 'POST':
        flash("POST validation failed", category = 'warning')

    if(session.get('username') == None):
        return render_template('contact.html', form=form, username="Guest")
    
    form.name.data = session.get('username')
    form.email.data = session.get('email')
    return render_template('contact.html', form=form, username=session.get('username'))

@cabinet_bp.route('/delete_session')
def delete_session():
    session.pop('username', default=None)
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'

@cabinet_bp.route('/database')
def database() :
    contacts = Contact.query.all()
    return render_template('database.html', contacts=contacts)


@cabinet_bp.route('/database/delete/<id>')
def delete_by_id(id):
    data = Contact.query.get(id)
    try:
        db.session.delete(data)
        db.session.commit()
    except :
        db.session.flush()
        db.session.rollback()   
    return redirect(url_for("cabinet.database"))

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
