# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request, redirect, url_for  
import os
import datetime as dt
app = Flask(__name__) 

osname = os.name
oslog = os.getlogin()
osid = os.getpid()
os_info = [osname,oslog,osid]

@app.route('/education')
def education():
    date = dt.datetime.now()
    return render_template('education.html', user_info=request.headers.get('User-Agent'),os_info=os_info,date=date)

@app.route('/portfolio')
def portfolio():
    return redirect(url_for('home'))

@app.route('/hobbies')
def hobbies():
    date = dt.datetime.now()
    return render_template('hobbies.html', user_info=request.headers.get('User-Agent'),os_info=os_info,date=date)


@app.route('/')
def home():  
    date = dt.datetime.now()
    return render_template('index.html',name='Yevhen Brusak', user_info=request.headers.get('User-Agent'),os_info=os_info,date=date)


if __name__ == '__main__': 
    app.run(debug=True)
