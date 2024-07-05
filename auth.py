from flask import Blueprint, render_template, request, redirect, flash, make_response
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, RegistrationForm
from .models import User, UserRoles
from . import db
import pickle
import base64
import os

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        flash('You have been logged in!') # Template missing for this

        response = make_response(redirect('/'))
        serialized_data = pickle.dumps(user.username)
        display = base64.b64encode(serialized_data).decode('utf-8')
        # This is a terrible idea, but I don't know how to fix it
        response.set_cookie('display_name', display)

        return response
    else:
        flash('Please check your login details and try again.')
        #return 'Invalid login'
        return redirect('/login')
    return redirect('/')

@auth.route('/logout',methods=['GET'])
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('display_name', '', expires=0)
    logout_user()
    return response

@auth.route('/register',methods=['GET'])
def get_register():
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('register.html')

@auth.route('/register',methods=['POST'])
def register_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    try:
        role = request.form['role'] # Future proofing
    except:
        role = 0
    user = User.query.filter_by(email=email).first()

    print(request.form)
    if user:
        flash('Email address already exists')
        return redirect('/register')

    new_user = User(email=email, password=password, username=username)
    db.session.add(new_user)
    db.session.commit()

    new_user_id = User.query.filter_by(email=email).first().id
    new_user_role = UserRoles(user_id=new_user_id, role_id=role)
    db.session.add(new_user_role)
    db.session.commit()

    return redirect('/login')   
