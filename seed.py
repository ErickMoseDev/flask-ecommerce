from models import db, Customer
from app import app


with app.app_context():
    # delete previous data
    print("Removing previous data 🌱...")
    Customer.query.delete()
    # db.session.query(Customer).delete()

    # add customers
    customer1 = Customer(
        first_name="Jane",
        last_name="Doe",
        email="janedoe@gmail.com",
        phone="0786543218",
        gender="Female",
        age=27,
    )
    customer2 = Customer(
        first_name="Johnny",
        last_name="Boy",
        email="johnnyboy@gmail.com",
        phone="0712345678",
        gender="Male",
        age=30,
    )
    customer3 = Customer(
        first_name="Hope",
        last_name="Yunia",
        email="hope@gmail.com",
        phone="0712389745",
        gender="Female",
        age=24,
    )
    customer4 = Customer(
        first_name="Masela",
        last_name="Ogendo",
        email="masela@gmail.com",
        phone="0712354321",
        gender="Female",
        age=25,
    )
    customer5 = Customer(
        first_name="Eugene",
        last_name="Wekesa",
        email="eugene@gmail.com",
        phone="0743529875",
        gender="Male",
        age=45,
    )

    # save the data into the database
    db.session.add_all([customer1, customer2, customer3, customer4, customer5])
    db.session.commit()
    # commit()
    print("Database Seeded Successfully! 🌱")
