# ===============================================================================
# Vehicle routes blueprints
# ===============================================================================

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.vehicle import Vehicle
from schemas.vehicle import VehicleSchema

vehicle_bp = Blueprint('vehicles', __name__)


# Get all vehicles with pagination
# ===============================================================================
@vehicle_bp.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Get all vehicles with pagination."""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    vehicles_paginated = Vehicle.query.paginate(page=page, per_page=limit, error_out=False)

    vehicle_schema = VehicleSchema(many=True)
    result = vehicle_schema.dump(vehicles_paginated.items)

    response = {
        'vehicles': result,
        'total_vehicles': vehicles_paginated.total,
        'total_pages': vehicles_paginated.pages,
        'current_page': vehicles_paginated.page,
        'has_next': vehicles_paginated.has_next,
        'has_prev': vehicles_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# Search vehicles by brand or model with pagination
# ===============================================================================
@vehicle_bp.route('/api/vehicles/search', methods=['GET'])
def search_vehicles():
    """Search vehicles by brand or model with pagination."""
    # Get query parameters
    query = request.args.get('q', '', type=str)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    # If query is empty, return all vehicles (same as get_vehicles)
    if not query.strip():
        return get_vehicles()

    # Search by brand or model (case-insensitive)
    search_filter = db.or_(
        Vehicle.brand.ilike(f'%{query}%'),
        Vehicle.model.ilike(f'%{query}%')
    )

    # Paginate filtered results
    vehicles_paginated = Vehicle.query.filter(search_filter).paginate(
        page=page, per_page=limit, error_out=False
    )

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


# Get vehicle by ID
# ===============================================================================
@vehicle_bp.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get a specific vehicle by ID."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    # Serialize policies
    policies = []
    for p in vehicle.policies:
        policies.append({
            "policy_id": p.policy_id,
            "status": p.status,
            "start_date": p.start_date.isoformat() if p.start_date else None,
            "end_date": p.end_date.isoformat() if p.end_date else None,
        })

    title = f"{vehicle.brand} {vehicle.model} ({vehicle.year})"

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


# Create vehicle
# ===============================================================================
@vehicle_bp.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    """Create a new vehicle."""
    data = request.get_json()
    vehicle_schema = VehicleSchema()
    new_vehicle = vehicle_schema.load(data)
    db.session.add(new_vehicle)
    db.session.commit()
    result = vehicle_schema.dump(new_vehicle)
    return make_response(jsonify({'message': 'Vehicle created successfully', 'vehicle': result}), 201)


# Update vehicle
# ===============================================================================
@vehicle_bp.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update an existing vehicle."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()
    
    vehicle_schema = VehicleSchema()
    updated_vehicle = vehicle_schema.load(data, instance=vehicle, partial=True)
    
    db.session.commit()
    result = vehicle_schema.dump(updated_vehicle)
    
    return make_response(jsonify({'message': 'Vehicle updated successfully', 'vehicle': result}), 200)


# Delete vehicle
# ===============================================================================
@vehicle_bp.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    db.session.delete(vehicle)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Vehicle deleted successfully'}), 200)
