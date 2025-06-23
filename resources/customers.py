from flask import make_response, request
from flask_restful import Resource

from models import db, Customer


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
            return make_response(response, 400)

        except Exception as e:
            response = {
                "code": 500,
                "message": "An error occured",
                "error": f"{str(e)}",
            }
            return make_response(response, 500)


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
