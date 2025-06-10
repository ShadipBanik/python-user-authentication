from flask import Blueprint, flash, render_template, request,redirect,url_for
from .models import User 
from werkzeug.security import generate_password_hash,check_password_hash
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['post','get'])
def login():
     data = request.form
     print(data)
     return render_template('login.html', boolean=True)

@auth.route('/logout')
def logOut():
    return '<h1>Log Out</h1>'

@auth.route('/signUp', methods = ['post','get'])
def signUp():
     if request.method == 'POST':

         email = request.form.get('email')
         firstName = request.form.get('firstName')
         lastName = request.form.get('lastName')
         password = request.form.get('password')
         confirmPassword = request.form.get('confirmPassword')

         if len(email)<4:
              flash('Email must be greater than 3 characters', category = 'error')
         elif len(firstName)<2:
              flash('Firstname must be greater than 2 characters', category = 'error')    
         elif password != confirmPassword:
              flash('password must be at least 7 characters ', category = 'error')      
         elif len(password)<7:
              flash('pasword dont match', category = 'error') 
         else:
              new_user = User(email=email,firstName = firstName,lastName = lastName, password = generate_password_hash(password, method='sha256'))
              db.session.add(new_user)
              db.session.commit()
              flash('acount created!', category='success')
              return redirect(url_for('views.home'))
     return render_template('sign-up.html')

    