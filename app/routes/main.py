from flask import Blueprint, render_template, current_app, redirect, url_for, flash, session, request
import pandas as pd
from app.forms.forms import AccountForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes.login_required import login_required
from app.scripts.log import event_logging
from datetime import datetime

main = Blueprint('main', __name__)

def authenticate_user(username, password, db):
    """
    Authenticate user credentials.
    Returns the user document if valid, else None.
    """
    user = db['users'].find_one({'username': username}) or db['accounts'].find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return user
    return None

@main.route("/")
@login_required
def index():
    # Check if fbclid is in the query parameters
    fbclid = request.args.get('fbclid')

    if fbclid:
        # If fbclid is present, you can log it, pass it on, or perform a redirect.
        # Here we just append it to the URL and redirect to the same route without fbclid in the query
        return redirect(url_for('main.index', _external=True))

    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    total_orders = 0
    cursor = db.orders.aggregate([
        {"$match": {'user_id': user_id, 'account_id': account_id}},
        {'$group': {'_id': None, 'total': {'$sum': '$net_price'}}}
    ])
    try:
        total_orders = cursor.next().get('total', 0)
    except StopIteration:
        total_orders = 0

    total_orders_quantity = 0
    cursor = db.orders.aggregate([
        {"$match": {'user_id': user_id, 'account_id': account_id}},
        {'$group': {'_id': None, 'total': {'$sum': 1}}}
    ])
    try:
        total_orders_quantity = cursor.next().get('total', 0)
    except StopIteration:
        total_orders_quantity = 0

    total_products = db.products.count_documents({
        'user_id': user_id,
        'account_id': account_id
    })

    total_cogs = 0
    cursor = db.orders.aggregate([
        {"$match": {'user_id': user_id, 'account_id': account_id}},
        {'$group': {'_id': None, 'total': {'$sum': '$price'}}}
    ])
    try:
        total_cogs = cursor.next().get('total', 0)
    except StopIteration:
        total_cogs = 0

    revenue = total_orders - total_cogs

    try:
        roi = (revenue/total_cogs) * 100
    except Exception as e:
        roi = 0
        flash(f"No available COGs data yet, you may add them to see your ROI.", "danger")
    
    return render_template("dashboard.html", title="Dashboard", 
                           total_orders=total_orders, 
                           total_products=total_products,
                           total_cogs=total_cogs,
                           total_orders_quantity=total_orders_quantity,
                           revenue=revenue,
                           roi=roi)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db = current_app.db
        username = form.username.data.strip()
        password = form.password.data.strip()
        
        user = authenticate_user(username, password, db)
        if user:
            session['user_id'] = user.get('user_id') or None
            session['is_admin'] = user.get('is_admin', False)
            session['account_id'] = user.get('account_id', None)

            flash("Login successful!", "success")
            event_logging(event_var="login",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=None,
                        old_doc=None,
                        new_doc=None,
                        error=None)
            return redirect(url_for('main.index'))
        else:
            flash("Invalid username or password. Please try again.", "danger")
    
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.", "info")
    event_logging(event_var="logout",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=None,
                old_doc=None,
                new_doc=None,
                error=None)
    return redirect(url_for('main.login'))  # Redirect to login page

@main.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    form = AccountForm()
    db = current_app.db

    if form.validate_on_submit():
        if db.accounts.find_one({'username': form.username.data}):
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('main.admin_signup'))
        
        hashed_password = generate_password_hash(form.password.data)
        count_docs = db.accounts.count_documents({})
        
        new_record = {
            'date_inserted': datetime.now(),
            'account_id': count_docs,
            'username': form.username.data.strip(),
            'password': hashed_password,
            'name': form.name.data.strip().title(),
            'email': form.email.data.strip().lower(),
            'subscription': form.subscription.data,
            'is_admin': True
        }

        result = db.accounts.insert_one(new_record)
        result_id = result.inserted_id
        new_record['_id'] = result_id
            
        event_logging(event_var="admin signup",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=result_id,
                    old_doc=None,
                    new_doc=new_record,
                    error=None)

        flash("Admin account created successfully!", "success")
        return redirect(url_for('main.login'))

    return render_template('admin_signup.html', form=form)

