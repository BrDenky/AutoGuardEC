"""
Claim routes blueprint.
"""

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.claim import Claim
from schemas.claim import ClaimSchema

claim_bp = Blueprint('claims', __name__)


@claim_bp.route('/api/claims/', methods=['GET'])
def get_claims():
    """Get all claims with pagination."""
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


@claim_bp.route('/api/claims/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    """Get a specific claim by ID."""
    claim = Claim.query.get_or_404(claim_id)

    # Serialize claim payments
    claim_payments = [
        {
            "claim_payment_id": cp.claim_payment_id,
            "payment_date": cp.payment_date.isoformat(),
            "amount": float(cp.amount)
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


@claim_bp.route('/api/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    """Update an existing claim."""
    claim = Claim.query.get_or_404(claim_id)
    data = request.get_json()

    schema = ClaimSchema()
    updated_claim = schema.load(data, instance=claim, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Claim updated successfully",
        "claim": schema.dump(updated_claim)
    }), 200)


@claim_bp.route('/api/claims/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    """Delete a claim."""
    claim = Claim.query.get_or_404(claim_id)
    db.session.delete(claim)
    db.session.commit()
    return make_response(jsonify({"message": "Claim deleted successfully"}), 200)
