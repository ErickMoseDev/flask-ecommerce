from flask import Flask, make_response, request
from flask_migrate import Migrate
from werkzeug.exceptions import BadRequest

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
@app.post("/customers")
def add_customer():
    # get the data from the request
    # verify that the data you are getting from the user is the right format
    # save that data in the database

    try:
        data = request.get_json()

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        phone = data.get("phone")
        gender = data.get("gender")
        age = data.get("age")

        # create an isntance of the Customer class
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            age=age,
        )

        # add the details to out database
        db.session.add(customer)
        db.session.commit()

        response = {
            "code": 201,
            "message": "Customer account created successfully",
        }

        return make_response(response, 201)

    except Exception as e:
        response = {"code": 400, "message": "An error occured", "error": f"{str(e)}"}

        return make_response(response, 400)


# perfom patch operations
# partial updates -> write the logic to account for this
# delete operations


@app.get("/customers")
def get_all_customers():
    # query the database and retrieve all the customers
    # return the data in a format that other applications can understand
    # customers = db.session.query(Customer).all()
    customers = Customer.query.all()
    # customer_list = [customer.to_dict() for customer in customers]
    # the other way
    cust_list = []
    for customer in customers:
        # cust = {
        #     "id": customer.id,
        #     "first_name": customer.first_name,
        #     "last_name": customer.last_name,
        #     "email": customer.email,
        #     "phone": customer.phone,
        #     "gender": customer.gender,
        #     "age": customer.age,
        # }
        # cust_list.append(
        #     customer.to_dict(only=("first_name", "gender", "last_name", "email"))
        # )
        cust_list.append(customer.to_dict(rules=("-created_at", "-phone", "-id")))

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
        # customer_dict = {
        #     "id": customer.id,
        #     "first_name": customer.first_name,
        #     "last_name": customer.last_name,
        #     "email": customer.email,
        #     "phone": customer.phone,
        #     "gender": customer.gender,
        #     "age": customer.age,
        # }
        return make_response(customer.to_dict(), 200)
    else:
        return make_response({"status": 404, "message": "No customer found"}, 404)


# perform patch request
@app.patch("/customers/<int:id>")
def update_customer(id):
    try:
        customer = Customer.query.get(id)

        if customer:
            # retrieve the data sent from the client
            data = request.get_json()

            for attr in data:
                setattr(customer, attr, request.get_json().get(attr))

            db.session.add(customer)
            db.session.commit()

            resp = {
                "status": "Successful",
                "message": "Customer updated successfully",
                "code": 200,
            }

            return make_response(resp, 200)
        else:
            resp = {
                "status": "Successful",
                "message": f"No customer found with id {id}",
                "code": 404,
            }

            return make_response(resp, 404)
    except BadRequest as b:
        resp = {
            "error": f"Error: {str(b)}",
            "message": "Invalid request",
            "code": 400,
        }
        return make_response(resp, 400)
    except Exception as e:
        resp = {
            "error": f"Error: {str(e)}",
            "message": "Internal server error",
            "code": 500,
        }
        return make_response(resp, 500)
