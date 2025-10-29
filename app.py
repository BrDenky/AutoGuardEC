# Import necessary libraries
from flask import Flask, jsonify, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# Connection with docker proyect
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3307/CarInsuranceDB?charset=utf8mb4'

db = SQLAlchemy(app)


# Models

class Customer(db.Model):
    __tablename__ = 'Customer'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, first_name, last_name, address, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.email = email


class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    vehicle_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    license_plate = db.Column(db.String(20), unique=True)

    def __init__(self, customer_id, brand, model, year, license_plate):
        self.customer_id = customer_id
        self.brand = brand
        self.model = model
        self.year = year
        self.license_plate = license_plate


class Policy(db.Model):
    __tablename__ = 'Policy'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    policy_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.vehicle_id'))
    agent_id = db.Column(db.Integer)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('active', 'expired', 'canceled', 'arrears'))

    def __init__(self, customer_id, vehicle_id, agent_id,
                 start_date, end_date, status):
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.agent_id = agent_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status


# Marshmallow Schemas

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True


class VehicleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True


class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        load_instance = True


# Initialize Database---------------------

with app.app_context():
    db.create_all()

# Tables Endpoints (GET AND POST)

# Customer Table
# Endpoint GET authors con Schema
@app.route('/api/customers', methods=['GET'])
def get_customers():
    get_customers = Customer.query.all()
    customers_schema = CustomerSchema(many=True)
    result = customers_schema.dump(get_customers)
    return make_response(jsonify({'customers': result}), 200)


@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer_schema = CustomerSchema()
    new_customer = customer_schema.load(data)
    db.session.add(new_customer)
    db.session.commit()
    result = customer_schema.dump(new_customer)
    return make_response(jsonify({'message': 'Customer created successfully', 'customer': result}), 201)


# Vehicle Table
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    get_vehicles = Vehicle.query.all()
    vehicle_schema = VehicleSchema(many=True)
    result = vehicle_schema.dump(get_vehicles)
    return make_response(jsonify({'vehicles': result}), 200)


@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    vehicle_schema = VehicleSchema()
    new_vehicle = vehicle_schema.load(data)
    db.session.add(new_vehicle)
    db.session.commit()
    result = vehicle_schema.dump(new_vehicle)
    return make_response(jsonify({'message': 'Vehicle created successfully', 'vehicle': result}), 201)


# Policy Table
@app.route('/api/policies', methods=['GET'])
def get_policies():
    get_policies = Policy.query.all()
    policy_schema = PolicySchema(many=True)
    result = policy_schema.dump(get_policies)
    return make_response(jsonify({'policies': result}), 200)


@app.route('/api/policies', methods=['POST'])
def create_policy():
    data = request.get_json()
    policy_schema = PolicySchema()
    new_policy = policy_schema.load(data)
    db.session.add(new_policy)
    db.session.commit()
    result = policy_schema.dump(new_policy)
    return make_response(jsonify({'message': 'Policy created successfully', 'policy': result}), 201)



# Communication with FrontEnd routes
# ============================
# FRONTEND ROUTES (GUI)
# ============================
@app.route('/')
def home():
    return render_template('index.html', title="Car Insurance System")

@app.route('/customers')
def customers_view():
    return render_template('customers.html', title="Customers")

@app.route('/vehicles')
def vehicles_view():
    return render_template('vehicles.html', title="Vehicles")

@app.route('/policies')
def policies_view():
    return render_template('policies.html', title="Policies")















if __name__ == '__main__':
    app.run(debug=True)