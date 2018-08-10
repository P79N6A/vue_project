"""Session Tables Mixin.

Provides an interface so that table queries, creates, updates,
and deletes are done through a proxy table for the purposes of
demonstrating the admin app on my homepage.

This entire file is pretty much a sequence of nasty hacks.

"""

import time

from flask import session, request
from sqlalchemy import event

from .models import (
    db, Category, Customer, Order, Product,
    ProductCategory, Review, Sale, Supplier)


class SessionTablesMixin():
    """Session Tables setup."""

    def __init__(self, app):
        self.app = app
        self.db = db
        self.old_query = self.db.session.query
        self.model_list = [
            Category, Customer, Order, Product,
            ProductCategory, Review, Sale, Supplier
        ]

        self.initialize_hooks()

    def initialize_hooks(self):
        # Request hook for table setup on new user.
        self.app.before_request(self.table_setup_2)

        # Query and join override to add session filter.
        self.db.session.query = self.query_override

        # Create event mappers for increment and session_id association.
        self.associate_mappers()

    def table_setup_2(self):
        if "loading" not in request.path and "id_tracking" not in session:
            tracking_dict = dict()
            # Query category and see if any old records exist for this session.
            last_category_obj = self.db.session.query(
                Category
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Category.id.desc()
            ).first()

            if last_category_obj is None:
                # For each 'real' table, create copy entries in session tables.
                # Use raw sql to avoid MetaData namespace conflicts.

                # Categories
                self.db.session.execute("""
                    INSERT INTO
                        "category_session"
                        (id, name, description, timestamp_deleted, session_id)
                    SELECT
                        category.id, category.name, category.description, category.timestamp_deleted, :session_id
                    FROM
                        category
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Customers
                self.db.session.execute("""
                    INSERT INTO
                        "customer_session"
                        (id, first_name, last_name, address, city, state, zip_code, phone, email, password_hash, session_id)
                    SELECT
                        customer.id, customer.first_name, customer.last_name, customer.address, customer.city, customer.state, customer.zip_code, customer.phone, customer.email, customer.password_hash, :session_id
                    FROM
                        customer
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Orders
                self.db.session.execute("""
                    INSERT INTO
                        "order_session"
                        (id, sale_id, customer_id, timestamp_created, session_id)
                    SELECT
                        "order".id, "order".sale_id, "order".customer_id, "order".timestamp_created, :session_id
                    FROM
                        "order"
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Products
                self.db.session.execute("""
                    INSERT INTO
                        "product_session"
                        (id, name, supplier_id, units_in_stock, unit_price, part_number, image_name, image, session_id)
                    SELECT
                        product.id, product.name, product.supplier_id, product.units_in_stock, product.unit_price, product.part_number, product.image_name, product.image, :session_id
                    FROM
                        product
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Product Categories
                self.db.session.execute("""
                    INSERT INTO
                        "product_category_session"
                        (id, category_id, product_id, session_id)
                    SELECT
                        product_category.id, product_category.category_id, product_category.product_id, :session_id
                    FROM
                        product_category
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Reviews
                self.db.session.execute("""
                    INSERT INTO
                        "review_session"
                        (id, customer_id, product_id, rating, review, timestamp_created, shown, session_id)
                    SELECT
                        review.id, review.customer_id, review.product_id, review.rating, review.review, review.timestamp_created, review.shown, :session_id
                    FROM
                        review
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Sales
                self.db.session.execute("""
                    INSERT INTO
                        "sale_session"
                        (id, product_id, price, timestamp_created, timestamp_ended, session_id)
                    SELECT
                        sale.id, sale.product_id, sale.price, sale.timestamp_created, sale.timestamp_ended, :session_id
                    FROM
                        sale
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

                # Suppliers
                self.db.session.execute("""
                    INSERT INTO
                        "supplier_session"
                        (id, name, contact_name, contact_title, address, city, zip_code, state, phone, contact_phone, contact_email, session_id)
                    SELECT
                        supplier.id, supplier.name, supplier.contact_name, supplier.contact_title, supplier.address, supplier.city, supplier.zip_code, supplier.state, supplier.phone, supplier.contact_phone, supplier.contact_email, :session_id
                    FROM
                        supplier
                """, {
                    "session_id": session.sid
                })

                self.db.session.commit()

            # Populate tracking dictionary

            # Categories
            last_obj = self.db.session.query(
                Category
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Category.id.desc()
            ).first()
            tracking_dict["category_session"] = last_obj.id

            # Customers
            last_obj = self.db.session.query(
                Customer
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Customer.id.desc()
            ).first()
            tracking_dict["customer_session"] = last_obj.id

            # Orders
            last_obj = self.db.session.query(
                Order
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Order.id.desc()
            ).first()
            tracking_dict["order_session"] = last_obj.id

            # Products
            last_obj = self.db.session.query(
                Product
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Product.id.desc()
            ).first()
            tracking_dict["product_session"] = last_obj.id

            # Product Categories
            last_obj = self.db.session.query(
                ProductCategory
            ).filter_by(
                session_id=session.sid
            ).order_by(
                ProductCategory.id.desc()
            ).first()
            tracking_dict["product_category_session"] = last_obj.id

            # Reviews
            last_obj = self.db.session.query(
                Review
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Review.id.desc()
            ).first()
            tracking_dict["review_session"] = last_obj.id

            # Sales
            last_obj = self.db.session.query(
                Sale
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Sale.id.desc()
            ).first()
            tracking_dict["sale_session"] = last_obj.id

            # Suppliers
            last_obj = self.db.session.query(
                Supplier
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Supplier.id.desc()
            ).first()
            tracking_dict["supplier_session"] = last_obj.id

            session["id_tracking"] = tracking_dict

    def table_setup(self):
        if "loading" not in request.path and "id_tracking" not in session:
            tracking_dict = dict()
            # Query category and see if any old records exist for this session.
            last_category_obj = self.db.session.query(
                Category
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Category.id.desc()
            ).first()

            if last_category_obj is None:
                # For each 'real' table, create copy entries in session tables.
                # Use raw sql to avoid MetaData namespace conflicts.

                # Categories
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM category
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Category(
                        ind_obj.name,
                        ind_obj.description,
                        ind_obj.timestamp_deleted,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Customers
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM customer
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Customer(
                        ind_obj.email,
                        ind_obj.password_hash,
                        ind_obj.first_name,
                        ind_obj.last_name,
                        ind_obj.address,
                        ind_obj.city,
                        ind_obj.state,
                        ind_obj.zip_code,
                        ind_obj.phone,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Orders
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM "order"
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Order(
                        ind_obj.sale_id,
                        ind_obj.customer_id,
                        ind_obj.timestamp_created,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Products
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM product
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Product(
                        ind_obj.name,
                        ind_obj.supplier_id,
                        ind_obj.units_in_stock,
                        ind_obj.unit_price,
                        ind_obj.part_number,
                        ind_obj.image_name,
                        ind_obj.image,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Product Categories
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM product_category
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = ProductCategory(
                        ind_obj.category_id,
                        ind_obj.product_id,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Reviews
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM review
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Review(
                        ind_obj.customer_id,
                        ind_obj.product_id,
                        ind_obj.rating,
                        ind_obj.review,
                        ind_obj.timestamp_created,
                        ind_obj.shown,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Sales
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM sale
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Sale(
                        ind_obj.product_id,
                        ind_obj.price,
                        ind_obj.timestamp_created,
                        ind_obj.timestamp_ended,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

                # Suppliers
                real_objs = self.db.session.execute('''
                    SELECT *
                    FROM supplier
                ''')
                for ind_obj in real_objs:
                    new_faux_obj = Supplier(
                        ind_obj.name,
                        ind_obj.contact_name,
                        ind_obj.contact_title,
                        ind_obj.address,
                        ind_obj.city,
                        ind_obj.zip_code,
                        ind_obj.state,
                        ind_obj.phone,
                        ind_obj.contact_phone,
                        ind_obj.contact_email,
                        ind_obj.id,
                        session.sid
                    )
                    self.db.session.add(new_faux_obj)
                    self.db.session.commit()

            # Populate tracking dictionary

            # Categories
            last_obj = self.db.session.query(
                Category
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Category.id.desc()
            ).first()
            tracking_dict["category_session"] = last_obj.id

            # Customers
            last_obj = self.db.session.query(
                Customer
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Customer.id.desc()
            ).first()
            tracking_dict["customer_session"] = last_obj.id

            # Orders
            last_obj = self.db.session.query(
                Order
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Order.id.desc()
            ).first()
            tracking_dict["order_session"] = last_obj.id

            # Products
            last_obj = self.db.session.query(
                Product
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Product.id.desc()
            ).first()
            tracking_dict["product_session"] = last_obj.id

            # Product Categories
            last_obj = self.db.session.query(
                ProductCategory
            ).filter_by(
                session_id=session.sid
            ).order_by(
                ProductCategory.id.desc()
            ).first()
            tracking_dict["product_category_session"] = last_obj.id

            # Reviews
            last_obj = self.db.session.query(
                Review
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Review.id.desc()
            ).first()
            tracking_dict["review_session"] = last_obj.id

            # Sales
            last_obj = self.db.session.query(
                Sale
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Sale.id.desc()
            ).first()
            tracking_dict["sale_session"] = last_obj.id

            # Suppliers
            last_obj = self.db.session.query(
                Supplier
            ).filter_by(
                session_id=session.sid
            ).order_by(
                Supplier.id.desc()
            ).first()
            tracking_dict["supplier_session"] = last_obj.id

            session["id_tracking"] = tracking_dict

    def query_override(self, *args, **kwargs):
        base_query = self.old_query(*args, **kwargs)

        # Apply session_id filter
        if args[0].__tablename__ in [x.__tablename__ for x in self.model_list]:
            base_query = base_query.filter(args[0].session_id == session.sid)

        # Apply session_id filter on joins from /query_x/ routes
        if "query_" in request.path:
            if args[0].__tablename__ in ["order_session"]:
                base_query = base_query.filter(
                    Customer.session_id == session.sid
                )
            elif args[0].__tablename__ in ["sale_session"]:
                base_query = base_query.filter(
                    Product.session_id == session.sid
                )

        return base_query

    def associate_mappers(self):
        for model in self.model_list:
            event.listen(model, "before_insert", self.create_mapper)

    def create_mapper(self, mapper, connection, target):
        if target.__tablename__ in [
            x.__tablename__ for x in self.model_list
        ] and "id_tracking" in session:
            # Assign session_id
            target.session_id = session.sid

            # Iterate id
            current_id = session["id_tracking"][target.__tablename__]
            session["id_tracking"][target.__tablename__] = current_id + 1
            target.id = current_id + 1
