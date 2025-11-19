# dot.env - Producción
# ------------------------------------------------------------------------
import os
from dotenv import load_dotenv
load_dotenv()

# Import necessary libraries
# ------------------------------------------------------------------------
from flask import Flask, jsonify, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

# Import and logic to implement OPENAI - API KEY
# ------------------------------------------------------------------------
#import openai
#load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")


# APP and Docker Configuration
# ------------------------------------------------------------------------
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# Connection with docker proyect
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
#'mysql+pymysql://root:123@localhost:3307/CarInsuranceDB?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3307/CarInsuranceDB?charset=utf8mb4'
db = SQLAlchemy(app)



# Prueba AGENTE INTELIGENTE
# ------------------------------------------------------------------------
#from ai_agent import ai_bp
#app.register_blueprint(ai_bp)


# Create all Models/Tables to manage data
# ------------------------------------------------------------------------
class Customer(db.Model):
    __tablename__ = 'Customer'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    # Relación
    vehicles = db.relationship('Vehicle', back_populates='customer', cascade='all, delete-orphan')
    policies = db.relationship('Policy', back_populates='customer', cascade='all, delete-orphan')

class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    vehicle_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    license_plate = db.Column(db.String(20), unique=True)

    # Relación
    customer = db.relationship('Customer', back_populates='vehicles')
    policies = db.relationship('Policy', back_populates='vehicle', cascade='all, delete-orphan')

class Agent(db.Model):
    __tablename__ = 'Agent'
    __table_args__ = { 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    agent_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    # Relación
    policies = db.relationship('Policy', back_populates='agent', cascade='all, delete-orphan')

class Coverage(db.Model):
    __tablename__ = 'Coverage'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    coverage_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)

    # Relación
    policies = db.relationship('Policy', secondary='PolicyCoverage', back_populates='coverages')


class PremiumPayment(db.Model):
    __tablename__ = 'PremiumPayment'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    payment_id = db.Column(db.Integer, primary_key = True)
    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'))
    payment_date = db.Column(db.String(100), nullable = False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Relación
    policy = db.relationship('Policy', back_populates='premium_payments')


class Claim(db.Model):
    __tablename__ = 'Claim'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    claim_id = db.Column(db.Integer, primary_key = True)
    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'))
    claim_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable = False)
    status = db.Column(db.Enum('open', 'closed', 'in review'))

    # Relación
    policy = db.relationship('Policy', back_populates='claims')
    claim_payments = db.relationship('ClaimPayment', back_populates='claim', cascade='all, delete-orphan')


class ClaimPayment(db.Model):
    __tablename__ = 'ClaimPayment'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    claim_payment_id = db.Column(db.Integer, primary_key = True)
    claim_id = db.Column(db.Integer, db.ForeignKey('Claim.claim_id'))
    payment_date = db.Column(db.Date, nullable = False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Relación
    claim = db.relationship('Claim', back_populates='claim_payments')

class PolicyCoverage(db.Model):
    __tablename__ = 'PolicyCoverage'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'), primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('Coverage.coverage_id'), primary_key=True)









class Policy(db.Model):
    __tablename__ = 'Policy'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    policy_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.vehicle_id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('Agent.agent_id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('active', 'expired', 'canceled', 'arrears'))

    # Relación
    customer = db.relationship('Customer', back_populates='policies')
    vehicle = db.relationship('Vehicle', back_populates='policies')
    agent = db.relationship('Agent', back_populates='policies')
    coverages = db.relationship('Coverage', secondary='PolicyCoverage', back_populates='policies')
    claims = db.relationship('Claim', back_populates='policy', cascade='all, delete-orphan')
    premium_payments = db.relationship('PremiumPayment', back_populates='policy', cascade='all, delete-orphan')



# Marshmallow Schemas to manage communication with SQL-ALCHEMY with JSON
# ------------------------------------------------------------------------
class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True


class VehicleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        include_fk = True
        load_instance = True


class AgentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Agent
        include_fk = True
        load_instance = True


class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        include_fk = True
        load_instance = True


class CoverageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Coverage
        include_fk = True
        load_instance = True


class PremiumPaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PremiumPayment
        include_fk = True
        load_instance = True


class ClaimSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Claim
        include_fk = True
        load_instance = True


class ClaimPaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ClaimPayment
        include_fk = True
        load_instance = True


class PolicyCoverageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PolicyCoverage
        include_fk = True
        load_instance = True


# Initialize Database
# ------------------------------------------------------------------------

with app.app_context():
    db.create_all()


# Necessary Endpoints to manage al interaction with Database
# GET, POST, PUT, DELETE
# ------------------------------------------------------------------------

# CUSTOMER TABLE
# ------------------------------------------------------------------------
# GET with pagination
# ========================================================================
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

# GET customer by ID
# ========================================================================
# @app.route('/api/customers/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     customer_schema = CustomerSchema()
#     result = customer_schema.dump(customer)
#     return make_response(jsonify({'customer': result}), 200)

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    # Construir nombre completo
    full_name = f"{customer.first_name} {customer.last_name}"

    # Serializar vehículos del cliente
    vehicles = []
    for v in customer.vehicles:
        vehicles.append({
            "vehicle_id": v.vehicle_id,
            "brand": v.brand,
            "model": v.model,
            "year": v.year,
            "license_plate": v.license_plate
        })

    # JSON que EXACTAMENTE espera el modal
    response = {
        "customer_id": customer.customer_id,
        "name": full_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "vehicles": vehicles
    }

    return jsonify(response), 200

# POST customer
# ========================================================================
@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer_schema = CustomerSchema()
    new_customer = customer_schema.load(data)
    db.session.add(new_customer)
    db.session.commit()
    result = customer_schema.dump(new_customer)
    return make_response(jsonify({'message': 'Customer created successfully', 'customer': result}), 201)

# PUT customer
# ========================================================================
@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    customer_schema = CustomerSchema()
    updated_customer = customer_schema.load(data, instance=customer, partial=True)
    
    db.session.commit()
    result = customer_schema.dump(updated_customer)
    
    return make_response(jsonify({'message': 'Customer updated successfully', 'customer': result}), 200)

# DELETE customer
# ========================================================================
@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    db.session.delete(customer)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Customer deleted successfully'}), 200)


# VEHICLE TABLE
# ------------------------------------------------------------------------
# GET vehicles with pagination
# ========================================================================
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

# GET vehicle by ID
# ========================================================================
# @app.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
# def get_vehicle(vehicle_id):
#     vehicle = Vehicle.query.get_or_404(vehicle_id)
#     vehicle_schema = VehicleSchema()
#     result = vehicle_schema.dump(vehicle)
#     return make_response(jsonify({'vehicle': result}), 200)

@app.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    # Serializar pólizas del vehículo
    policies = []
    for p in vehicle.policies:
        policies.append({
            "policy_id": p.policy_id,
            "status": p.status,
            "start_date": p.start_date.isoformat() if p.start_date else None,
            "end_date": p.end_date.isoformat() if p.end_date else None,
        })

    # Título para el modal (Brand Model Year)
    title = f"{vehicle.brand} {vehicle.model} ({vehicle.year})"

    # JSON EXACTAMENTE como lo espera vehicle_quickview.js
    response = {
        "vehicle_id": vehicle.vehicle_id,
        "customer_id": vehicle.customer_id,
        "title": title,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "license_plate": vehicle.license_plate,
        "policies": policies
    }

    return jsonify(response), 200


# POST vehicle
# ========================================================================
@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    vehicle_schema = VehicleSchema()
    new_vehicle = vehicle_schema.load(data)
    db.session.add(new_vehicle)
    db.session.commit()
    result = vehicle_schema.dump(new_vehicle)
    return make_response(jsonify({'message': 'Vehicle created successfully', 'vehicle': result}), 201)

# PUT vehicle
# ========================================================================
@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()
    
    vehicle_schema = VehicleSchema()
    updated_vehicle = vehicle_schema.load(data, instance=vehicle, partial=True)
    
    db.session.commit()
    result = vehicle_schema.dump(updated_vehicle)
    
    return make_response(jsonify({'message': 'Vehicle updated successfully', 'vehicle': result}), 200)

# DELETE vehicle
# ========================================================================
@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    db.session.delete(vehicle)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Vehicle deleted successfully'}), 200)



# POLICY TABLE
# ------------------------------------------------------------------------
# GET policies with paginization
# ========================================================================
@app.route('/api/policies/', methods=['GET'])
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

# GET policy by ID
# ========================================================================
# @app.route('/api/policies/<int:policy_id>', methods=['GET'])
# def get_policy(policy_id):
#     policy = Policy.query.get_or_404(policy_id)
#     policy_schema = PolicySchema()
#     result = policy_schema.dump(policy)
#     return make_response(jsonify({'policy': result}), 200)

@app.route('/api/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)

    # Serialize customer
    customer = {
        "customer_id": policy.customer.customer_id,
        "name": f"{policy.customer.first_name} {policy.customer.last_name}"
    }

    # Serialize vehicle
    vehicle = {
        "vehicle_id": policy.vehicle.vehicle_id,
        "brand": policy.vehicle.brand,
        "model": policy.vehicle.model,
        "license_plate": policy.vehicle.license_plate
    }

    # Serialize agent
    agent = {
        "agent_id": policy.agent.agent_id,
        "name": policy.agent.name
    }

    # Serialize coverages
    coverages = [
        {
            "coverage_id": c.coverage_id,
            "name": c.name,
            "type": c.type if hasattr(c, "type") else None
        } for c in policy.coverages
    ]

    # Serialize claims
    claims = [
        {
            "claim_id": cl.claim_id,
            "status": cl.status
        } for cl in policy.claims
    ]

    # Serialize premium payments
    premium_payments = [
        {
            "payment_id": p.payment_id,
            "amount": p.amount
        } for p in policy.premium_payments
    ]

    response = {
        "policy_id": policy.policy_id,
        "start_date": policy.start_date.isoformat(),
        "end_date": policy.end_date.isoformat(),
        "status": policy.status,
        "customer": customer,
        "vehicle": vehicle,
        "agent": agent,
        "coverages": coverages,
        "claims": claims,
        "premium_payments": premium_payments
    }

    return jsonify(response), 200


# POST policy
# ========================================================================
@app.route('/api/policies', methods=['POST'])
def create_policy():
    data = request.get_json()
    policy_schema = PolicySchema()
    new_policy = policy_schema.load(data)
    db.session.add(new_policy)
    db.session.commit()
    result = policy_schema.dump(new_policy)
    return make_response(jsonify({'message': 'Policy created successfully', 'policy': result}), 201)

# PUT policy
# ========================================================================
@app.route('/api/policies/<int:policy_id>', methods=['PUT'])
def update_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    data = request.get_json()
    
    policy_schema = PolicySchema()
    updated_policy = policy_schema.load(data, instance=policy, partial=True)
    
    db.session.commit()
    result = policy_schema.dump(updated_policy)
    
    return make_response(jsonify({'message': 'Policy updated successfully', 'policy': result}), 200)

# DELETE policy
# ========================================================================
@app.route('/api/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    
    db.session.delete(policy)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Policy deleted successfully'}), 200)

# AGENT TABLE
# ------------------------------------------------------------------------
# GET agent with paginization
# ========================================================================
@app.route('/api/agents/', methods=['GET'])
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

# GET agent by ID
# ========================================================================
# @app.route('/api/agents/<int:agent_id>', methods=['GET'])
# def get_agent(agent_id):
#     agent = Agent.query.get_or_404(agent_id)
#     agent_schema = AgentSchema()
#     result = agent_schema.dump(agent)
#     return make_response(jsonify({'agent': result}), 200)

@app.route('/api/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)

    # Serializar pólizas asignadas al agente
    policies = []
    for p in agent.policies:
        policies.append({
            "policy_id": p.policy_id,
            "status": getattr(p, "status", None),
            "start_date": p.start_date.isoformat() if getattr(p, "start_date", None) else None,
            "end_date": p.end_date.isoformat() if getattr(p, "end_date", None) else None
        })

    response = {
        "agent_id": agent.agent_id,
        "name": agent.name,
        "email": agent.email,
        "phone": agent.phone,
        "policies": policies
    }

    return jsonify(response), 200


# POST agent
# ========================================================================
@app.route('/api/agents', methods=['POST'])
def create_agent():
    data = request.get_json()
    agent_schema = AgentSchema()
    new_agent = agent_schema.load(data)
    db.session.add(new_agent)
    db.session.commit()
    result = agent_schema.dump(new_agent)
    return make_response(jsonify({'message': 'Agent created successfully', 'agent': result}), 201)

# PUT agent
# ========================================================================
@app.route('/api/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    agent_schema = AgentSchema()
    updated_agent = agent_schema.load(data, instance=agent, partial=True)

    db.session.commit()
    result = agent_schema.dump(updated_agent)

    return make_response(jsonify({'message': 'Agent updated successfully', 'agent': result}), 200)

# DELETE agent
# ========================================================================
@app.route('/api/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return make_response(jsonify({'message': 'Agent deleted successfully'}), 200)


# COVERAGE TABLE
# ------------------------------------------------------------------------
# GET coverage
# ========================================================================
@app.route('/api/coverages/', methods=['GET'])
def get_coverages():
    # Query params
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # Pagination
    coverages_paginated = Coverage.query.paginate(page=page, per_page=limit, error_out=False)

    # Serialization
    schema = CoverageSchema(many=True)
    result = schema.dump(coverages_paginated.items)

    # Response
    response = {
        "coverages": result,
        "total_coverages": coverages_paginated.total,
        "total_pages": coverages_paginated.pages,
        "current_page": coverages_paginated.page,
        "has_next": coverages_paginated.has_next,
        "has_prev": coverages_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET coverage by ID
# ========================================================================
@app.route('/api/coverages/<int:coverage_id>', methods = ['GET'])
def get_coverage(coverage_id):
    coverage = Coverage.query.get_or_404(coverage_id)
    coverage_schema = CoverageSchema()
    result = coverage_schema.dump(coverage)
    return make_response(jsonify({"coverage": result}), 200)

# PUT coverage
# ========================================================================
@app.route('/api/coverages/<int:coverage_id>', methods = ['PUT'])
def update_coverage(coverage_id):
    coverage = Coverage.query.get_or_404(coverage_id)
    data = request.get_json()

    coverage_schema = CoverageSchema()
    updated_coverage = coverage_schema.load(data, instance=coverage, partial=True)

    db.session.commit()
    result = coverage_schema.dump(updated_coverage)

    return make_response(jsonify({'message' : 'Coverage updated successfully', 'coverage' : result}), 200)

# DELETE coverage
# ========================================================================
@app.route('/api/coverages/<int:coverage_id>', methods = ['DELETE'])
def delete_coverage(coverage_id):
    coverage = Coverage.query.get_or_404(coverage_id)
    db.session.delete(coverage)
    db.session.commit()
    return make_response(jsonify({'message' : 'Coverage deleted successfully'}), 200)





# PREMIUM PAYMENTS ENDPOINTS
# ------------------------------------------------------------------------
# GET all premium payments
# ========================================================================
@app.route('/api/premium_payments/', methods=['GET'])
def get_premium_payments():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    payments_paginated = PremiumPayment.query.paginate(page=page, per_page=limit, error_out=False)

    schema = PremiumPaymentSchema(many=True)
    result = schema.dump(payments_paginated.items)

    response = {
        "premium_payments": result,
        "total_payments": payments_paginated.total,
        "total_pages": payments_paginated.pages,
        "current_page": payments_paginated.page,
        "has_next": payments_paginated.has_next,
        "has_prev": payments_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET premium payment by ID
# ========================================================================
@app.route('/api/premium_payments/<int:payment_id>', methods=['GET'])
def get_premium_payment(payment_id):
    payment = PremiumPayment.query.get_or_404(payment_id)
    schema = PremiumPaymentSchema()
    return make_response(jsonify({"premium_payment": schema.dump(payment)}), 200)

# PUT premium payment
# ========================================================================
@app.route('/api/premium_payments/<int:payment_id>', methods=['PUT'])
def update_premium_payment(payment_id):
    payment = PremiumPayment.query.get_or_404(payment_id)
    data = request.get_json()

    schema = PremiumPaymentSchema()
    updated = schema.load(data, instance=payment, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Premium payment updated successfully",
        "premium_payment": schema.dump(updated)
    }), 200)

# DELETE premium payment
# ========================================================================
@app.route('/api/premium_payments/<int:payment_id>', methods=['DELETE'])
def delete_premium_payment(payment_id):
    payment = PremiumPayment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return make_response(jsonify({"message": "Premium payment deleted successfully"}), 200)




# CLAIMS ENDPOINTS
# ------------------------------------------------------------------------
# GET all claims
# ========================================================================
@app.route('/api/claims/', methods=['GET'])
def get_claims():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    claims_paginated = Claim.query.paginate(page=page, per_page=limit, error_out=False)

    schema = ClaimSchema(many=True)
    result = schema.dump(claims_paginated.items)

    response = {
        "claims": result,
        "total_claims": claims_paginated.total,
        "total_pages": claims_paginated.pages,
        "current_page": claims_paginated.page,
        "has_next": claims_paginated.has_next,
        "has_prev": claims_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET claim by ID
# ========================================================================
# @app.route('/api/claims/<int:claim_id>', methods=['GET'])
# def get_claim(claim_id):
#     claim = Claim.query.get_or_404(claim_id)
#     schema = ClaimSchema()
#     return make_response(jsonify({"claim": schema.dump(claim)}), 200)

@app.route('/api/claims/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)

    # Serialize claim payments
    claim_payments = [
        {
            "claim_payment_id": cp.claim_payment_id,
            "payment_date": cp.payment_date.isoformat(),
            "amount": float(cp.amount)  # convertir Decimal → float
        }
        for cp in claim.claim_payments
    ]

    response = {
        "claim_id": claim.claim_id,
        "policy_id": claim.policy_id,
        "claim_date": claim.claim_date.isoformat(),
        "description": claim.description,
        "status": claim.status,
        "claim_payments": claim_payments
    }

    return jsonify(response), 200



# PUT claim
# ========================================================================
@app.route('/api/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    data = request.get_json()

    schema = ClaimSchema()
    updated_claim = schema.load(data, instance=claim, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Claim updated successfully",
        "claim": schema.dump(updated_claim)
    }), 200)

# DELETE claim
# ========================================================================
@app.route('/api/claims/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    db.session.delete(claim)
    db.session.commit()
    return make_response(jsonify({"message": "Claim deleted successfully"}), 200)






# CLAIM PAYMENTS ENDPOINTS
# ------------------------------------------------------------------------
# GET all claim payments
# ========================================================================
@app.route('/api/claim_payments/', methods=['GET'])
def get_claim_payments():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    payments_paginated = ClaimPayment.query.paginate(page=page, per_page=limit, error_out=False)

    schema = ClaimPaymentSchema(many=True)
    result = schema.dump(payments_paginated.items)

    response = {
        "claim_payments": result,
        "total_payments": payments_paginated.total,
        "total_pages": payments_paginated.pages,
        "current_page": payments_paginated.page,
        "has_next": payments_paginated.has_next,
        "has_prev": payments_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET claim payment by ID
# ========================================================================
@app.route('/api/claim_payments/<int:payment_id>', methods=['GET'])
def get_claim_payment(payment_id):
    payment = ClaimPayment.query.get_or_404(payment_id)
    schema = ClaimPaymentSchema()
    return make_response(jsonify({"claim_payment": schema.dump(payment)}), 200)

# PUT claim payment
# ========================================================================
@app.route('/api/claim_payments/<int:payment_id>', methods=['PUT'])
def update_claim_payment(payment_id):
    payment = ClaimPayment.query.get_or_404(payment_id)
    data = request.get_json()

    schema = ClaimPaymentSchema()
    updated = schema.load(data, instance=payment, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Claim payment updated successfully",
        "claim_payment": schema.dump(updated)
    }), 200)

# DELETE claim payment
# ========================================================================
@app.route('/api/claim_payments/<int:payment_id>', methods=['DELETE'])
def delete_claim_payment(payment_id):
    payment = ClaimPayment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return make_response(jsonify({"message": "Claim payment deleted successfully"}), 200)





# ========================================================================
# POLICY COVERAGES ENDPOINTS
# ========================================================================

# GET all policy coverages
@app.route('/api/policy_coverages/', methods=['GET'])
def get_policy_coverages():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    pc_paginated = PolicyCoverage.query.paginate(page=page, per_page=limit, error_out=False)

    schema = PolicyCoverageSchema(many=True)
    result = schema.dump(pc_paginated.items)

    response = {
        "policy_coverages": result,
        "total_policy_coverages": pc_paginated.total,
        "total_pages": pc_paginated.pages,
        "current_page": pc_paginated.page,
        "has_next": pc_paginated.has_next,
        "has_prev": pc_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# GET policy coverage by ID
@app.route('/api/policy_coverages/<int:pc_id>', methods=['GET'])
def get_policy_coverage(pc_id):
    pc = PolicyCoverage.query.get_or_404(pc_id)
    schema = PolicyCoverageSchema()
    return make_response(jsonify({"policy_coverage": schema.dump(pc)}), 200)

# PUT policy coverage
@app.route('/api/policy_coverages/<int:pc_id>', methods=['PUT'])
def update_policy_coverage(pc_id):
    pc = PolicyCoverage.query.get_or_404(pc_id)
    data = request.get_json()

    schema = PolicyCoverageSchema()
    updated = schema.load(data, instance=pc, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Policy coverage updated successfully",
        "policy_coverage": schema.dump(updated)
    }), 200)

# DELETE policy coverage
@app.route('/api/policy_coverages/<int:pc_id>', methods=['DELETE'])
def delete_policy_coverage(pc_id):
    pc = PolicyCoverage.query.get_or_404(pc_id)
    db.session.delete(pc)
    db.session.commit()
    return make_response(jsonify({"message": "Policy coverage deleted successfully"}), 200)










# DATA ANALISYS SECTION
# ========================================================================
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
# ========================================================================
# FRONTEND ROUTES (GUI)
# ========================================================================
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

@app.route('/coverages')
def coverages_view():
    return render_template('coverages.html', title="Coverages")

@app.route('/premium_payments')
def premium_payments_view():
    return render_template('premiumpayments.html', title="Premium_Payments")

@app.route('/claims')
def claims_view():
    return render_template('claims.html', title="Claims")

@app.route('/claim_payment')
def claim_payments_view():
    return render_template('claimpayments.html', title="Claim_Payment")

@app.route('/policy_coverages')
def policy_coverages_view():
    return render_template('policycoverages.html', title="Policy_Coverages")


#@app.route("/ai_agent")
#def agent_page():
#    return render_template("ai_agent.html")
















if __name__ == '__main__':
    app.run(debug=True)