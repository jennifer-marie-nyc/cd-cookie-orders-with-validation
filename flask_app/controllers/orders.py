from flask import render_template, redirect, request, url_for, session
from flask_app import app
from flask_app.models.order import Order

@app.route('/cookies')
def display_orders():
    all_orders = Order.get_all()
    return render_template('orders.html', orders=all_orders)

@app.route('/cookies/new', methods=['GET', 'POST'])
def new_order():
    if request.method == 'GET':
        return render_template('new_order.html')
    elif request.method == 'POST':
        if not Order.validate_order(request.form):
            """If validations fail, save form data to session"""
            session['create_order_data'] = request.form
            return redirect('/cookies/new')
        """Upon successful form submission, remove create_order_data from session"""
        if 'create_user_data' in session:
            session.pop('create_order_data')
        Order.create(request.form)
        return redirect(url_for('display_orders'))
    
@app.route('/cookies/edit/<int:order_id>', methods = ['GET', 'POST'])
def edit_order(order_id):
    if request.method == 'GET':
        this_order = Order.get_one(order_id)
        return render_template('edit_order.html', order=this_order)
    if request.method == 'POST':
        if not Order.validate_order(request.form):
            return redirect(f'/cookies/edit/{order_id}')
        Order.update(request.form)
        return redirect(url_for('display_orders'))
        
