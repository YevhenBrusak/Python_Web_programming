from flask import render_template, request, redirect, url_for
from flask_login import current_user
import os
from loguru import logger
import datetime as dt

from . import home_bp

logger.add("my.log")

@home_bp.route('/education')
def education():
    return render_template('education.html')

@home_bp.route('/portfolio')
def portfolio():
    return redirect(url_for('home.home'))

@home_bp.route('/hobbies')
def hobbies():
    return render_template('hobbies.html',)


@home_bp.route('/')
def home():  
    return render_template('index.html',name='Yevhen Brusak')
