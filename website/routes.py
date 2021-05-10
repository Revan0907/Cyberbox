from website.models import User, Anonymous, Items, Orders
from flask import render_template, url_for, session
from website import app
from website import db
from flask import request, redirect, flash, request
from website.forms import RegistrationForm, LoginForm, PaymentForm
from flask_login import login_user, logout_user, current_user, login_required
import time

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get():
    return session.get('key', 'not set')

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    data = Items.query.all()
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    default = 'id'
    sort_by = request.form.get('sort_by', default)
    return render_template('home.html', data=data, default=sort_by)

@app.route("/product<int:item_id>", methods=['GET'])
def product(item_id):
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    data = Items.query.get(item_id)
    return render_template('product.html', data=data)

@app.route("/cart", methods=['GET','POST'])
def cart():
    if current_user.is_anonymous == True:
        return render_template('403.html'), 403

    if  not session["cart"] and not session["wish"]:
        flash("Cart is empty")
        return render_template('cart.html', display_cart = {}, total = 0, display_wish= {})
    
    elif session["wish"] and not session["cart"]:
        wishes = session["wish"]
        dict_of_wishes = {}
        for item in wishes:
            product = Items.query.get(item)
            dict_of_wishes[product.id] = {"id":product.id, "name": product.name, "price": product.price}
        return render_template('cart.html', display_cart = {}, total = 0, display_wish= dict_of_wishes)

    elif session["cart"] and not session["wish"]:
        items = session["cart"]
        dict_of_items = {}
        total_price = 0
        for item in items:
            product = Items.query.get(item)
            total_price += product.price
            if product.id in dict_of_items:
                dict_of_items[product.id]["qty"] +=1
            else:
                dict_of_items[product.id] = {"id":product.id, "name": product.name, "price": product.price, "qty":1}
        return render_template('cart.html', display_cart = dict_of_items, total = total_price, display_wish= {})
        
    else:
        items = session["cart"]
        wishes = session["wish"]
        dict_of_wishes = {}
        dict_of_items = {}
        total_price = 0
                
        for item in items:
            product = Items.query.get(item)
            total_price += product.price
            if product.id in dict_of_items:
                dict_of_items[product.id]["qty"] +=1
            else:
                dict_of_items[product.id] = {"id":product.id, "name": product.name, "price": product.price, "qty":1}

        for item in wishes:
            product = Items.query.get(item)
            dict_of_wishes[product.id] = {"id":product.id, "name": product.name, "price": product.price}
        return render_template('cart.html', display_cart = dict_of_items, total = total_price, display_wish=dict_of_wishes)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    if "wish" not in session:
        session["wish"] = []
    
    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route("/del_from_cart/<int:id>")
def del_from_cart(id):
    if "cart" not in session:
        session["cart"] = []
    if "wish" not in session:
        session["wish"] = []
        
    session["cart"].remove(id)

    flash("Successfully removed from cart!")
    return redirect("/cart")

@app.route("/del_fully_from_cart/<int:id>")
def del_fully_from_cart(id):
    if "cart" not in session:
        session["cart"] = []
    if "wish" not in session:
        session["wish"] = []

    num = session["cart"].count(id)
    for i in range(num):  
        session["cart"].remove(id)

    flash("Successfully removed from cart!")
    return redirect("/cart")

@app.route("/add_to_wish/<int:id>")
def add_to_wish(id):
    if "wish" not in session:
        session["wish"] = []
    if "cart" not in session:
        session["cart"] = []
    
    session["wish"].append(id)

    flash("Successfully added to wishlist!")
    return redirect("/cart")

@app.route("/add_to_cart_from_wish/<int:id>")
def add_to_cart_from_wish(id):
    if "wish" not in session:
        session["wish"] = []
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    session["wish"].remove(id)

    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if current_user.is_anonymous == True:
        return render_template('403.html'), 403
    form = PaymentForm()
    if form.validate_on_submit():
        cart = session.get("cart")
        string_ints = [str(int) for int in cart]
        newcart = (" ".join(string_ints))
        order = Orders(username = session.get("username"), address= form.address.data, shipment=newcart)
        db.session.add(order)
        db.session.commit()
        flash("Payment Successful! We'll get in touch shortly about your expected arrival date")
        session["cart"] = []
        time.sleep(3)
        return redirect("/home")
    return render_template('payment.html', form=form)

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
        flash('Account successfully created! Please login')
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
            session["username"] = user.username
            return redirect(url_for('home'))
        else:
           error = 'Invalid credentials'
    return render_template('login.html', title='Login', form=form,error=error)

@app.route("/logout")
def logout():
    logout_user()
    session.pop("cart", None)
    return redirect(url_for('home'))

@app.route("/403")
def error403():
    if current_user.is_anonymous == True:
        current_user.firstname = 'Guest'
    return render_template('403.html')

