# ===============================================================================
# Policy routes blueprints
# ===============================================================================

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.policy import Policy
from schemas.policy import PolicySchema

policy_bp = Blueprint('policies', __name__)


# Get all policies with pagination
# ===============================================================================
@policy_bp.route('/api/policies/', methods=['GET'])
def get_policies():
    """Get all policies with pagination."""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    policies_paginated = Policy.query.paginate(page=page, per_page=limit, error_out=False)

    policy_schema = PolicySchema(many=True)
    result = policy_schema.dump(policies_paginated.items)

    response = {
        'policies': result,
        'total_policies': policies_paginated.total,
        'total_pages': policies_paginated.pages,
        'current_page': policies_paginated.page,
        'has_next': policies_paginated.has_next,
        'has_prev': policies_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# Get policy by ID
# ===============================================================================
@policy_bp.route('/api/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    """Get a specific policy by ID."""
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


# Create policy
# ===============================================================================
@policy_bp.route('/api/policies', methods=['POST'])
def create_policy():
    """Create a new policy."""
    data = request.get_json()
    policy_schema = PolicySchema()
    new_policy = policy_schema.load(data)
    db.session.add(new_policy)
    db.session.commit()
    result = policy_schema.dump(new_policy)
    return make_response(jsonify({'message': 'Policy created successfully', 'policy': result}), 201)


# Update policy
# ===============================================================================
@policy_bp.route('/api/policies/<int:policy_id>', methods=['PUT'])
def update_policy(policy_id):
    """Update an existing policy."""
    policy = Policy.query.get_or_404(policy_id)
    data = request.get_json()
    
    policy_schema = PolicySchema()
    updated_policy = policy_schema.load(data, instance=policy, partial=True)
    
    db.session.commit()
    result = policy_schema.dump(updated_policy)
    
    return make_response(jsonify({'message': 'Policy updated successfully', 'policy': result}), 200)


# Delete policy
# ===============================================================================
@policy_bp.route('/api/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    """Delete a policy."""
    policy = Policy.query.get_or_404(policy_id)
    
    db.session.delete(policy)
    db.session.commit()
    
    return make_response(jsonify({'message': 'Policy deleted successfully'}), 200)
