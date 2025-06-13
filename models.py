from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# create the metadata instance
# metadata holds all the information about our table definitions, foreign keys, indexes, columns etc
metadata = MetaData()

# create the flask-sqlalchemy instance
db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f"<{self.first_name} {self.last_name}>"


# products
# orders
# order_items
# serialization with relationships
