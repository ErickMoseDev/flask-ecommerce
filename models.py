from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# create the metadata instance
# metadata holds all the information about our table definitions, foreign keys, indexes, columns etc

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(naming_convention=convention)

# create the flask-sqlalchemy instance
db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    serialize_rules = ("-orders.customer",)

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # relationships
    orders = db.relationship(
        "Order", back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<{self.first_name} {self.last_name}>"


class Product(db.Model, SerializerMixin):
    __tablename__ = "products"
    serialize_rules = ("-order_items.product",)

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # relationships
    order_items = db.relationship("OrderItem", back_populates="product")


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    serialize_rules = (
        "-customer.orders",
        "-order_items.order",
    )

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(db.String, nullable=False, default="pending")
    order_date = db.Column(db.DateTime(), default=datetime.now())
    total_amount = db.Column(db.Float, nullable=False)

    # foreign key
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    # relationships
    customer = db.relationship("Customer", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")


class OrderItem(db.Model, SerializerMixin):
    __tablename__ = "order_items"

    serialize_rules = (
        "-order.order_items",
        "-product.order_items",
    )

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # foreign keys
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # relationships
    product = db.relationship("Product", back_populates="order_items")
    order = db.relationship("Order", back_populates="order_items")


# products
# orders
# order_items
# serialization with relationships
