import re

from flask import make_response, request
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User


class Login(Resource):
    # parsing the arguments

    parser = reqparse.RequestParser()

    parser.add_argument("email", required=True, type=str, help="Email is required")

    def post(self):
        errors = []

        try:
            data = request.get_json()

            mail = data.get("email").lower()
            password = data.get("password")

            # validations

            if not mail or not mail.strip():
                errors.append("Email is required")
            else:
                regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

                if not re.match(regex, mail):
                    errors.append("Email is not valid")

            if not password or not password.strip():
                errors.append("Password is required")

            # we need to check if the user actually exists in the database
            user = User.query.filter_by(email=mail).first()

            if errors:
                response = {
                    "success": False,
                    "message": "Erros encountered",
                    "errors": errors,
                }

                return make_response(response, 400)

            # if everything checks out
            if user and check_password_hash(user.password, password):
                # generate access token
                access = create_access_token(identity=user.id)

                response = {
                    "message": "Login Successful",
                    "success": True,
                    "data": {"user": user.to_dict(), "access_token": access},
                }

                return make_response(response, 200)
            else:
                response = {
                    "success": False,
                    "message": "An error was encountered",
                    "errors": ["Invalid email or password"],
                }
                return make_response(response, 403)

        except Exception as e:
            errors.append(str(e))
            response = {
                "success": False,
                "message": "Internal server error",
                "errors": errors,
            }
            return make_response(response, 500)


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
            mail = data.get("email").lower()
            phone_number = data.get("phone")
            password = data.get("password")

            # validation checks - manual way
            if not f_name or not f_name.strip():
                errors.append("First name is required")
            if not l_name or not l_name.strip():
                errors.append("Last name is required")
            if not mail or not mail.strip():
                errors.append("Email is required")
            else:
                regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

                if not re.match(regex, mail):
                    errors.append("Email is not valid")

            if not phone_number or not phone_number.strip():
                errors.append("Phone number is required")
            else:
                if len(phone_number) < 10 or len(phone_number) > 10:
                    errors.append("Phone number must be 10 digits")

            if not password or not password.strip():
                errors.append("Password is required")

            # check for email and phone uniqueness
            email_check = User.query.filter_by(email=mail).first()
            phone_check = User.query.filter_by(phone=phone_number).first()

            if email_check:
                errors.append("Email adress already taken")
            if phone_check:
                errors.append("Phone number already taken")

            if errors:
                response = {
                    "success": False,
                    "message": "Erros encountered",
                    "errors": errors,
                }

                return make_response(response, 400)

            # handle the data once the validations pass
            # encrypt the password
            password_hash = generate_password_hash(password).decode("utf-8")

            # create a user instance
            user = User(
                first_name=f_name,
                last_name=l_name,
                email=mail,
                phone=phone_number,
                password=password_hash,
            )

            # add the user to the db
            db.session.add(user)
            db.session.commit()

            # create the access token
            access = create_access_token(identity=user.id)

            response = {
                "message": "User acount created successfully",
                "success": True,
                "data": {"user": user.to_dict(), "access_token": access},
            }
            return make_response(response, 201)

        except Exception as e:
            errors.append(str(e))
            response = {
                "success": False,
                "message": "Internal server error",
                "errors": errors,
            }
            return make_response(response, 500)
