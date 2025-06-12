from flask import Flask
from flask_migrate import Migrate

from models import db

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


@app.get("/customers")
def get_all_customers():
    pass
