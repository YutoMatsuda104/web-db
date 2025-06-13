from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_wtf.csrf import CSRFProtect

from forms import *
from models import *
import dataaccess as da

import os
import datetime
import pickle

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_ENABLED"] = True
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = da.auth(form.username.data, form.password.data)
        if user is None:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("login"))

        session["username"] = user.username
        session["cart"] = []
        return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    session.pop("cart", None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/additem", methods=["GET", "POST"])
def additem():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("login"))

    form = AddItemForm()

    if form.validate_on_submit():
        item = Item()
        form.copy_to(item)
        user = da.search_user(username=session["username"])
        item.owner_id = user.id
        da.add_item(item)
    
        flash("An item was added.", "info")
        return redirect(url_for("additem"))

    user = da.search_user(username=session["username"])
    item_list = da.search_items_by_owner_id(user.id)
    
    return render_template("additem.html", form=form, item_list=item_list)

@app.route("/searchitem", methods=["GET", "POST"])
def searchitem():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("login"))

    form = SearchItemForm()

    if form.validate_on_submit():
        item_list = da.search_items(form.itemname.data)
        session["item_list"] = pickle.dumps(item_list)
        return redirect(url_for("searchitem"))

    if "item_list" in session:
        item_list = pickle.loads(session["item_list"])
        session.pop("item_list", None)
    else:
        item_list = da.search_items("")

    return render_template("search.html", form=form, item_list=item_list)

@app.route("/addtocart", methods=["GET", "POST"])
def addtocart():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("login"))

    form = CheckOutForm()

    if request.args.get("item_id") is not None:
        item_id = request.args.get("item_id")
        item = da.search_item_by_id(item_id)

        if item is not None:
            cart = session["cart"]
            if cart is not None and len(cart) != 0:
                cart = pickle.loads(cart)
            cart.append(item)
            session["cart"] = pickle.dumps(cart)
            return redirect(url_for("addtocart"))

    cart = session["cart"]
    if cart is not None and len(cart) != 0:
        cart = pickle.loads(cart)

    return render_template("cart.html", form=form, item_list=cart)

@app.route("/removefromcart", methods=["GET", "POST"])
def removefromcart():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("login"))

    form = CheckOutForm()

    if request.args.get("index") is not None:
        index = int(request.args.get("index"))
        index = index - 1

        cart = session["cart"]
        if len(cart) != 0:
            cart = pickle.loads(cart)
        cart.pop(index)
        session["cart"] = pickle.dumps(cart)
        return redirect(url_for("removefromcart"))

    cart = session["cart"]
    if cart is not None and len(cart) != 0:
        cart = pickle.loads(cart)

    return render_template("cart.html", form=form, item_list=cart)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("login"))

    if "cart" in session:
        user = da.search_user(session["username"])
    
        cart = session["cart"]
        if cart is not None and len(cart) != 0:
            cart = pickle.loads(cart)
        
        order_list = []
        order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        for item in cart:
            order = Order() 
            order.order_code = order_code
            order.owner_id = item.owner_id
            order.ownername = item.ownername
            order.item_id = item.id
            order.itemname = item.itemname
            order.amount = 1
            order.price = item.price
            order_list.append(order)

        if len(order_list) != 0:
            da.add_order(order_list)
    
        session["cart"] = []
    
    return render_template("checkout.html", item_list=order_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)