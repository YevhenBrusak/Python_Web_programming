# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request, redirect, session, url_for, flash 
import os, logging
import datetime as dt
from forms import Myform

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'hala_madrid'

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
    main = logging.getLogger('main')
    main.setLevel(logging.DEBUG)
    handler=logging.FileHandler('my.log')
    format = logging.Formatter('%(asctime)s  %(name)s %(levelname)s: %(message)s')
    handler.setFormatter(format)
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        flash("Data sent successfully: " + session.get('username') + ' ' + session.get('email'), category = 'success')
        main.addHandler(handler)
        main.info(form.name.data + " " + form.email.data + " " + form.phone.data + " " + form.subject.data + " " + form.message.data)
        return redirect(url_for("contact"))

    elif request.method == 'POST':
        flash("POST validation failed", category = 'warning')
        main.addHandler(handler)
        main.error(form.name.data + " " + form.email.data + " " + form.phone.data + " " + form.subject.data + " " + form.message.data)

    if(session.get('username') == None):
        return render_template('contact.html', form=form, username="Guest")
    else :
        form.name.data = session.get('username')
        form.email.data = session.get('email')
        return render_template('contact.html', form=form, username=session.get('username'))


@app.route('/delete_session')
def delete_session():
    session.pop('username', default=None)
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'

@app.context_processor
def inject_user():
    date = dt.datetime.now()
    os_info = [os.name,os.getlogin(),os.getpid()]
    return dict(user_info=request.headers.get('User-Agent'),os_info=os_info,date=date)



if __name__ == '__main__': 
    app.run(debug=True)
