from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from models import db
from resources.customers import Customers, CustomerById
from resources.products import Products
from resources.auth import Login, Register

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

api.add_resource(Customers, "/customers")
api.add_resource(CustomerById, "/customers/<int:id>")
api.add_resource(Products, "/products")

# auth
api.add_resource(Login, "/login")
api.add_resource(Register, "/signup")
