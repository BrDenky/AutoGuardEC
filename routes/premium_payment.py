"""
PremiumPayment routes blueprint.
"""

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.premium_payment import PremiumPayment
from schemas.premium_payment import PremiumPaymentSchema

premium_payment_bp = Blueprint('premium_payments', __name__)


@premium_payment_bp.route('/api/premium_payments/', methods=['GET'])
def get_premium_payments():
    """Get all premium payments with pagination."""
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


@premium_payment_bp.route('/api/premium_payments/<int:payment_id>', methods=['GET'])
def get_premium_payment(payment_id):
    """Get a specific premium payment by ID."""
    payment = PremiumPayment.query.get_or_404(payment_id)
    schema = PremiumPaymentSchema()
    return make_response(jsonify({"premium_payment": schema.dump(payment)}), 200)


@premium_payment_bp.route('/api/premium_payments/<int:payment_id>', methods=['PUT'])
def update_premium_payment(payment_id):
    """Update an existing premium payment."""
    payment = PremiumPayment.query.get_or_404(payment_id)
    data = request.get_json()

    schema = PremiumPaymentSchema()
    updated = schema.load(data, instance=payment, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Premium payment updated successfully",
        "premium_payment": schema.dump(updated)
    }), 200)


@premium_payment_bp.route('/api/premium_payments/<int:payment_id>', methods=['DELETE'])
def delete_premium_payment(payment_id):
    """Delete a premium payment."""
    payment = PremiumPayment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return make_response(jsonify({"message": "Premium payment deleted successfully"}), 200)
