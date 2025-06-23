import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta

from models import db
from resources.customers import Customers, CustomerById
from resources.products import Products
from resources.auth import Login, Register


# load env vars
load_dotenv()

# heart of the flask application
app = Flask(__name__)

# setup a bcrypt instance
bcrypt = Bcrypt(app)

# database connection string
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")

# account for the token expiration
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# create a jwt instance for managing our jwt settings

jwt = JWTManager(app)

# instatiate Migrate class
migrate = Migrate(app=app, db=db)

# CORS
CORS(app=app)

# initialize our app
db.init_app(app=app)

# initialize api instance for adding resources
api = Api(app=app)


# jwt errors
@jwt.unauthorized_loader
def missing_token(error):
    return {
        "message": "Authorization required",
        "success": False,
        "errors": ["Authorization token is required"],
    }, 401


# define our routes

api.add_resource(Customers, "/customers")
api.add_resource(CustomerById, "/customers/<int:id>")
api.add_resource(Products, "/products")

# auth
api.add_resource(Login, "/login")
api.add_resource(Register, "/signup")


# refresh tokens
# blalcklisting token
# interceptors
