from website.models import User, Anonymous, Items
from flask import render_template, url_for, flash
from website import app
from website import db
from flask import request, redirect, flash
from website.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
    data = Items.query.all()
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    return render_template('home.html', data=data)


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    error = None
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Successfully logged in')
            return redirect(url_for('home'))
        else:
           error = 'Invalid credentials'
    return render_template('login.html', title='Login', form=form,error=error)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/cart", methods=['GET','POST'])
def cart():
    return render_template('cart.html', title="Shopping Cart")
