from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models import db, Product


class Products(Resource):
    def get(self):
        products = Product.query.all()

        product_list = [product.to_dict() for product in products]

        return make_response(product_list, 200)

    @jwt_required()
    def post(self):
        # get the data from the client request
        try:
            data = request.get_json()

            name = data.get("name")
            desc = data.get("description")
            cat = data.get("category")
            price = data.get("price")
            quantity = data.get("quantity")
            image = data.get("image")
            rating = data.get("rating")

            product = Product(
                image=image,
                name=name,
                description=desc,
                category=cat,
                price=price,
                quantity=quantity,
                rating=rating,
            )

            db.session.add(product)
            db.session.commit()

            response = {
                "status": "successful",
                "code": 201,
                "message": "product added successfully",
            }

            return make_response(response, 201)
        except Exception as e:
            response = {
                "code": 500,
                "message": "An error occured",
                "error": f"{str(e)}",
            }
            return make_response(response, 500)
