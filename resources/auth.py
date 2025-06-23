from flask import make_response, request
from flask_restful import Resource


class Login(Resource):
    pass


class Register(Resource):
    # get data from the client
    # validate that data
    # save the data in our db
    # generate an access token for our user
    # give back the response to the client

    def post(self):
        errors = []  # unified error object

        try:
            data = request.get_json()

            f_name = data.get("first_name")
            l_name = data.get("last_name")
            mail = data.get("email")
            phone_number = data.get("phone")
            password = data.get("password")

            # validation checks - manual way
            if not f_name or not f_name.strip():
                errors.append("First name is required")
            if not l_name or not l_name.strip():
                errors.append("Last name is required")
            if not mail or not mail.strip():
                errors.append("Email is required")
            if not phone_number or not phone_number.strip():
                errors.append("Phone number is required")
            if not password or not password.strip():
                errors.append("Password is required")

            if errors:
                response = {
                    "success": False,
                    "message": "Erros encountered",
                    "errors": errors,
                }

                return make_response(response, 400)

        except Exception as e:
            errors.append(str(e))
            response = {
                "success": False,
                "message": "Internal server error",
                "errors": errors,
            }
            return make_response(response, 500)
