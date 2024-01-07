from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email has no registered account.', category='error')

    return render_template('login.html', user=current_user)


def verifySignUp(email: str, nickName: str, createPassword: str, confirmPassword: str):
    trigger = 'proceed'
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already has a registered Account.', category='error')
        trigger = 'emailExists'

    else:
        if len(nickName) < 3:
            flash('Nickname must be at least 3 characters.', category='error')
            trigger = ''

        if createPassword == nickName:
            flash('Password must not match Nickname.', category='error')
            trigger = ''
        if len(createPassword) < 7:
            flash('Password must at least be 7 characters.', category='error')
            trigger = ''
        if createPassword != confirmPassword:
            flash('Passwords do not match.', category='error')
            trigger = ''

    return trigger


@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        data = request.form
        # print(data)
        email = data['email']
        nickName = data['nickName']
        createPassword = data['createPassword']
        confirmPassword = data['confirmPassword']

        result = verifySignUp(email, nickName, createPassword, confirmPassword)
        if result == 'proceed':
            newUser = User(email=email, nickName=nickName, password=generate_password_hash(createPassword))
            db.session.add(newUser)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(newUser, remember=True)
            return redirect(url_for('views.home'))

        if result == 'emailExists':
            flash('Redirect to login page.', category='info')
            return redirect(url_for('auth.login'))

    return render_template('signUp.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
