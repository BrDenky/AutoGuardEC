"""
ClaimPayment routes blueprint.
"""

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.claim_payment import ClaimPayment
from schemas.claim_payment import ClaimPaymentSchema

claim_payment_bp = Blueprint('claim_payments', __name__)


@claim_payment_bp.route('/api/claim_payments/', methods=['GET'])
def get_claim_payments():
    """Get all claim payments with pagination."""
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


@claim_payment_bp.route('/api/claim_payments/<int:payment_id>', methods=['GET'])
def get_claim_payment(payment_id):
    """Get a specific claim payment by ID."""
    payment = ClaimPayment.query.get_or_404(payment_id)
    schema = ClaimPaymentSchema()
    return make_response(jsonify({"claim_payment": schema.dump(payment)}), 200)


@claim_payment_bp.route('/api/claim_payments/<int:payment_id>', methods=['PUT'])
def update_claim_payment(payment_id):
    """Update an existing claim payment."""
    payment = ClaimPayment.query.get_or_404(payment_id)
    data = request.get_json()

    schema = ClaimPaymentSchema()
    updated = schema.load(data, instance=payment, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Claim payment updated successfully",
        "claim_payment": schema.dump(updated)
    }), 200)


@claim_payment_bp.route('/api/claim_payments/<int:payment_id>', methods=['DELETE'])
def delete_claim_payment(payment_id):
    """Delete a claim payment."""
    payment = ClaimPayment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return make_response(jsonify({"message": "Claim payment deleted successfully"}), 200)
