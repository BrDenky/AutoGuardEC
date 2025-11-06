# dot.env
from dotenv import load_dotenv
load_dotenv()
# Import necessary libraries
from flask import Flask, jsonify, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

import os
from dotenv import load_dotenv
#import openai
#load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# Connection with docker proyect
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
#'mysql+pymysql://root:123@localhost:3307/CarInsuranceDB?charset=utf8mb4'
db = SQLAlchemy(app)



# Prueba AGENTE INTELIGENTE
#from ai_agent import ai_bp
#app.register_blueprint(ai_bp)









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


class Agent(db.Model):
    __tablename__ = 'Agent'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    agent_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, name, phone=None, email=None):
        self.name = name
        self.phone = phone
        self.email = email





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

class AgentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Agent
        load_instance = True


# Initialize Database---------------------

with app.app_context():
    db.create_all()

# Tables Endpoints (GET, POST, PUT, DELETE) ------------------------------------------------------ 

# Customer Table
# Endpoint GET customers con Schema
# Endpoint GET customers with pagination
@app.route('/api/customers', methods=['GET'])
def get_customers():
    # Get query parameters (default: page=1, limit=6)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # Paginate query (error_out=False evita excepciones si la página es inválida)
    customers_paginated = Customer.query.paginate(page=page, per_page=limit, error_out=False)

    # Serialize current page items
    customers_schema = CustomerSchema(many=True)
    result = customers_schema.dump(customers_paginated.items)

    # Build response with pagination metadata
    response = {
        'customers': result,
        'total_customers': customers_paginated.total,
        'total_pages': customers_paginated.pages,
        'current_page': customers_paginated.page,
        'has_next': customers_paginated.has_next,
        'has_prev': customers_paginated.has_prev
    }

    return make_response(jsonify(response), 200)

# Endpoint GET customer por ID con Schema
@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_schema = CustomerSchema()
    result = customer_schema.dump(customer)
    return make_response(jsonify({'customer': result}), 200)

# Endopoint POST customers con Schema
@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer_schema = CustomerSchema()
    new_customer = customer_schema.load(data)
    db.session.add(new_customer)
    db.session.commit()
    result = customer_schema.dump(new_customer)
    return make_response(jsonify({'message': 'Customer created successfully', 'customer': result}), 201)

# Endpoint PUT customers con Schema
@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    customer_schema = CustomerSchema()
    updated_customer = customer_schema.load(data, instance=customer, partial=True)
    
    db.session.commit()
    result = customer_schema.dump(updated_customer)
    
    return make_response(jsonify({'message': 'Customer updated successfully', 'customer': result}), 200)

# Endpoint DELETE customers con Schema
@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    db.session.delete(customer)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Customer deleted successfully'}), 200)


# Vehicle Table
# Endpoint GET vehicles con Schema
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    # Get query parameters (default: page=1, limit=6)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # Paginate query (error_out=False evita excepciones si la página es inválida)
    vehicles_paginated = Vehicle.query.paginate(page=page, per_page=limit, error_out=False)

    # Serialize current page items
    vehicle_schema = VehicleSchema(many=True)
    result = vehicle_schema.dump(vehicles_paginated.items)

    # Build response with pagination metadata
    response = {
        'vehicles': result,
        'total_vehicles': vehicles_paginated.total,
        'total_pages': vehicles_paginated.pages,
        'current_page': vehicles_paginated.page,
        'has_next': vehicles_paginated.has_next,
        'has_prev': vehicles_paginated.has_prev
    }

    return make_response(jsonify(response), 200)

# Endpoint GET vehicle por ID con Schema
@app.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle_schema = VehicleSchema()
    result = vehicle_schema.dump(vehicle)
    return make_response(jsonify({'vehicle': result}), 200)

# Endpoint POST vehicles con Schema
@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    vehicle_schema = VehicleSchema()
    new_vehicle = vehicle_schema.load(data)
    db.session.add(new_vehicle)
    db.session.commit()
    result = vehicle_schema.dump(new_vehicle)
    return make_response(jsonify({'message': 'Vehicle created successfully', 'vehicle': result}), 201)

# Endpoint PUT vehicles con Schema
@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()
    
    vehicle_schema = VehicleSchema()
    updated_vehicle = vehicle_schema.load(data, instance=vehicle, partial=True)
    
    db.session.commit()
    result = vehicle_schema.dump(updated_vehicle)
    
    return make_response(jsonify({'message': 'Vehicle updated successfully', 'vehicle': result}), 200)

# Endpoint DELETE vehicles con Schema
@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    db.session.delete(vehicle)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Vehicle deleted successfully'}), 200)



# Policy Table
# Endpoint GET policies con Schema
@app.route('/api/policies', methods=['GET'])
def get_policies():
    # Get query parameters (default: page=1, limit=6)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # Paginate query (error_out=False evita excepciones si la página es inválida)
    policies_paginated = Policy.query.paginate(page=page, per_page=limit, error_out=False)

    # Serialize current page items
    policy_schema = PolicySchema(many=True)
    result = policy_schema.dump(policies_paginated.items)

    # Build response with pagination metadata
    response = {
        'policies': result,
        'total_policies': policies_paginated.total,
        'total_pages': policies_paginated.pages,
        'current_page': policies_paginated.page,
        'has_next': policies_paginated.has_next,
        'has_prev': policies_paginated.has_prev
    }

    return make_response(jsonify(response), 200)

# Endpoint GET policy por ID con Schema
@app.route('/api/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    policy_schema = PolicySchema()
    result = policy_schema.dump(policy)
    return make_response(jsonify({'policy': result}), 200)

# Endpoint POST policies con Schema
@app.route('/api/policies', methods=['POST'])
def create_policy():
    data = request.get_json()
    policy_schema = PolicySchema()
    new_policy = policy_schema.load(data)
    db.session.add(new_policy)
    db.session.commit()
    result = policy_schema.dump(new_policy)
    return make_response(jsonify({'message': 'Policy created successfully', 'policy': result}), 201)

# Endpoint PUT policies con Schema
@app.route('/api/policies/<int:policy_id>', methods=['PUT'])
def update_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    data = request.get_json()
    
    policy_schema = PolicySchema()
    updated_policy = policy_schema.load(data, instance=policy, partial=True)
    
    db.session.commit()
    result = policy_schema.dump(updated_policy)
    
    return make_response(jsonify({'message': 'Policy updated successfully', 'policy': result}), 200)

# Endpoint DELETE policies con Schema
@app.route('/api/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    
    db.session.delete(policy)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Policy deleted successfully'}), 200)



# Agent Endpoints--------------------------------------------------------------------------------------------------

# GET - Paginated Agents
@app.route('/api/agents', methods=['GET'])
def get_agents():
    # Query parameters (default: page=1, limit=6)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # Paginate query
    agents_paginated = Agent.query.paginate(page=page, per_page=limit, error_out=False)

    # Serialize current page items
    agents_schema = AgentSchema(many=True)
    result = agents_schema.dump(agents_paginated.items)

    # Build response with pagination metadata
    response = {
        'agents': result,
        'total_agents': agents_paginated.total,
        'total_pages': agents_paginated.pages,
        'current_page': agents_paginated.page,
        'has_next': agents_paginated.has_next,
        'has_prev': agents_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET - Single Agent by ID
@app.route('/api/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    agent_schema = AgentSchema()
    result = agent_schema.dump(agent)
    return make_response(jsonify({'agent': result}), 200)


# POST - Create New Agent
@app.route('/api/agents', methods=['POST'])
def create_agent():
    data = request.get_json()
    agent_schema = AgentSchema()
    new_agent = agent_schema.load(data)
    db.session.add(new_agent)
    db.session.commit()
    result = agent_schema.dump(new_agent)
    return make_response(jsonify({'message': 'Agent created successfully', 'agent': result}), 201)



# PUT - Update Agent by ID
@app.route('/api/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    agent_schema = AgentSchema()
    updated_agent = agent_schema.load(data, instance=agent, partial=True)

    db.session.commit()
    result = agent_schema.dump(updated_agent)

    return make_response(jsonify({'message': 'Agent updated successfully', 'agent': result}), 200)


# DELETE - Remove Agent by ID
@app.route('/api/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return make_response(jsonify({'message': 'Agent deleted successfully'}), 200)












# DATA ANALISYS SECTION-----------------------------------------
@app.route('/api/dashboard-data')
def dashboard_data():
    stats = get_dashboard_stats()
    return jsonify(stats)


# SQLALCHEMY QUERIES TO DASHBOARD/Graphics
def get_dashboard_stats():
    stats = {
        'total_customers': db.session.query(Customer).count(),
        'total_vehicles': db.session.query(Vehicle).count(),
        'active_policies': db.session.query(Policy).filter(Policy.status == 'active').count(),
        'expired_policies': db.session.query(Policy).filter(Policy.status == 'expired').count(),
        'canceled_policies': db.session.query(Policy).filter(Policy.status == 'canceled').count(),
        'total_agents': db.session.query(Agent).count(),
    }
    
    # Calcular revenue
    #stats['monthly_revenue'] = stats['active_policies'] * 150  # Ejemplo
    
    return stats





# Communication with FrontEnd routes
# ============================
# FRONTEND ROUTES (GUI)
# ============================
@app.route('/')
def home():
    stats = get_dashboard_stats()
    return render_template('index.html', 
                         title="Car Insurance System",
                         **stats) # Give previusly calculated stats

@app.route('/customers')
def customers_view():
    return render_template('customers.html', title="Customers")

@app.route('/vehicles')
def vehicles_view():
    return render_template('vehicles.html', title="Vehicles")

@app.route('/policies')
def policies_view():
    return render_template('policies.html', title="Policies")

@app.route('/agents')
def agents_view():
    return render_template('agents.html', title="Agents")


#@app.route("/ai_agent")
#def agent_page():
#    return render_template("ai_agent.html")
















if __name__ == '__main__':
    app.run(debug=True)