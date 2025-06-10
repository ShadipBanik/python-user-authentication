from . import db
from flask import Blueprint, flash, render_template, request,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User 
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['post','get'])
def login():
     if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('password')
          user = User.query.filter_by(email = email).first()
          if user:
               if check_password_hash(user.password, password):
                    flash('Log in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
               else:
                    flash('wrong password. Please try with correct password', category='error')
          else:
               flash('email does not exist', category='error')

     return render_template('login.html', user = current_user)


@auth.route('/signUp', methods = ['post','get'])
def signUp():
     if request.method == 'POST':

         email = request.form.get('email')
         firstName = request.form.get('firstName')
         lastName = request.form.get('lastName')
         password = request.form.get('password')
         confirmPassword = request.form.get('confirmPassword')
         user = User.query.filter_by(email = email).first()

         if user:
              flash('This email already exist.please use new email!', category='error')
         elif len(email)<4:
              flash('Email must be greater than 3 characters', category = 'error')
         elif len(firstName)<2:
              flash('Firstname must be greater than 2 characters', category = 'error')    
         elif password != confirmPassword:
              flash('password must be at least 7 characters ', category = 'error')      
         elif len(password)<7:
              flash('pasword dont match', category = 'error') 
         else:
              
              new_user = User(email=email,firstName = firstName, lastName = lastName, password = generate_password_hash(password, method='pbkdf2:sha256'))
              db.session.add(new_user)
              db.session.commit()
              flash('acount created!', category='success')
              login_user(user, remember=True)
              return redirect(url_for('views.home'))
     return render_template('sign-up.html', user = current_user)

@auth.route('/logout')
@login_required   
def logOut():
    logout_user()
    return redirect(url_for('auth.login'))
