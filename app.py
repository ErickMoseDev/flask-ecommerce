from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Customer

# create a flask application instance / heart of the application
app = Flask(__name__)

# configure a database connection
# app.config

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# initialize flask migrate
migrate = Migrate(app=app, db=db)


# initalize the app to use sqlalchemy database
db.init_app(app=app)


# flask cli
# inform the cli about the flask app and the port to use

# app operations
# fetch all data from the db and return as JSON


# CRUD OPERATIONS ON CUSTOMERS
# CREATE A CUSTOMER
# RETRIEVE INFO ABOUT A CUSTOMER
# UPDATE A CUSTOMER
# DELETE A CUSTOMER


@app.get("/customers")
def get_all_customers():
    # query the database and retrieve all the customers
    # return the data in a format that other applications can understand
    # customers = db.session.query(Customer).all()
    customers = Customer.query.all()
    customer_list = [
        {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "gender": customer.gender,
            "age": customer.age,
        }
        for customer in customers
    ]
    # the other way
    cust_list = []
    for customer in customers:
        cust = {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "gender": customer.gender,
            "age": customer.age,
        }
        cust_list.append(cust)

    return make_response(cust_list, 200)


@app.get("/customers/<int:id>")
def get_one_customer(id):
    # query the databse and we get a customer by the customer id
    # if the customer exists -> return the details of that customer
    # else -> rreturn an appropriate response and the appropriate status code

    # .get(id)
    # technique 1
    # customer = Customer.query.get(id)

    # filter_by - technique 2
    customer = Customer.query.filter_by(id=id).first()

    if customer:
        customer_dict = {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "gender": customer.gender,
            "age": customer.age,
        }
        return make_response(customer_dict, 200)
    else:
        return make_response({"status": 404, "message": "No customer found"}, 404)


# post
# serialization to_dict()
