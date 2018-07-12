"""Session Tables Mixin.

Provides an interface so that table queries, creates, updates,
and deletes are done through a proxy table for the purposes of
demonstrating the admin app on my homepage.

This entire file is pretty much a sequence of nasty hacks.

"""

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
        self.app.before_request(self.table_setup)

        # Query and join override to add session filter.
        self.db.session.query = self.query_override

        # Create event mappers for increment and session_id association.
        self.associate_mappers()

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
