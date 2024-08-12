from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint

class Order:
    db = 'cookie_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']

    @staticmethod
    def create(form_data):
        query = """
        INSERT INTO orders
        (name, cookie_type, num_of_boxes)
        VALUES (%(name)s, %(cookie_type)s, %(num_of_boxes)s)
    """
        new_order_id = connectToMySQL('cookie_schema').query_db(query, form_data)

        return new_order_id

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM orders
        """
        results = connectToMySQL(cls.db).query_db(query)
        pprint(results)
        all_orders = []
        for row in results:
            all_orders.append(cls(row))
        
        return all_orders
    
    @classmethod
    def get_one(cls, order_id):
        query = """
        SELECT * FROM orders
        WHERE id = %(id)s;
    """
        data = {
            'id': order_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)
        this_order = cls(results[0])
        return this_order
    
    @staticmethod
    def update(form_data):
        query = """
            UPDATE orders
            SET name = %(name)s,
            cookie_type = %(cookie_type)s,
            num_of_boxes = %(num_of_boxes)s
            where id = %(id)s
        """
        connectToMySQL('cookie_schema').query_db(query, form_data)

    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(order['cookie_type']) < 2:
            flash('Cookie type must be at least 2 characters.')
            is_valid = False
        if not order['num_of_boxes']:
            flash('Number of boxes is required')
            is_valid = False
        elif float(order['num_of_boxes']) < 1:
            flash('Number of boxes must be greater than 0')
            is_valid = False
        return is_valid