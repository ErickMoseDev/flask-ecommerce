from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS

from models import db, Customer

# heart of the flask application
app = Flask(__name__)

# database connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# instatiate Migrate class
migrate = Migrate(app=app, db=db)

# CORS
CORS(app=app)

# initialize our app
db.init_app(app=app)

# initialize api instance for adding resources
api = Api(app=app)


# define our routes
# /customers
class Customers(Resource):
    def get(self):
        # get the data from the db
        customers = Customer.query.all()

        # convert the data into json format
        cust_list = []
        for customer in customers:
            cust_list.append(customer.to_dict())

        return make_response(cust_list, 200)

    def post(self):
        try:
            # get the data from the client
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
                "status": "successful",
                "code": 201,
                "message": "Customer account created successfully",
            }

            return make_response(response, 201)
        except ValueError as ve:
            response = {
                "code": 400,
                "message": "An error occured",
                "error": f"{str(ve)}",
            }

        except Exception as e:
            response = {
                "code": 500,
                "message": "An error occured",
                "error": f"{str(e)}",
            }

        return make_response(response, 400)


class CustomerById(Resource):
    def get(self, id):
        # customer = Customer.query.get(id)
        customer = Customer.query.filter_by(id=id).first()

        if customer:
            return make_response(customer.to_dict(), 200)
        else:
            return make_response(
                {"code": 404, "message": "No customer found", "status": "Unsuccessful"},
                404,
            )

    def patch(self, id):
        pass

    def delete(self, id):
        pass

    # def cool_patch(self, id):
    #     pass


api.add_resource(Customers, "/customers")
api.add_resource(CustomerById, "/customers/<int:id>")
