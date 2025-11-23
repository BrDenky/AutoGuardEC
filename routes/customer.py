"""
Customer routes blueprint.
"""

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.customer import Customer
from schemas.customer import CustomerSchema

customer_bp = Blueprint('customers', __name__)


@customer_bp.route('/api/customers', methods=['GET'])
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
# @customer_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     customer_schema = CustomerSchema()
#     result = customer_schema.dump(customer)
#     return make_response(jsonify({'customer': result}), 200)

@customer_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
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
@customer_bp.route('/api/customers', methods=['POST'])
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
@customer_bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
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
@customer_bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    db.session.delete(customer)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Customer deleted successfully'}), 200)
