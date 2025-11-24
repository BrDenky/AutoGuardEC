# ===============================================================================
# PolicyCoverage routes blueprints
# ===============================================================================

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.policy_coverage import PolicyCoverage
from schemas.policy_coverage import PolicyCoverageSchema

policy_coverage_bp = Blueprint('policy_coverages', __name__)


# Get all policy coverages with pagination
# ===============================================================================
@policy_coverage_bp.route('/api/policy_coverages/', methods=['GET'])
def get_policy_coverages():
    """Get all policy coverages with pagination."""
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


# Get policy coverage by ID
# ===============================================================================
@policy_coverage_bp.route('/api/policy_coverages/<int:pc_id>', methods=['GET'])
def get_policy_coverage(pc_id):
    """Get a specific policy coverage by ID."""
    pc = PolicyCoverage.query.get_or_404(pc_id)
    schema = PolicyCoverageSchema()
    return make_response(jsonify({"policy_coverage": schema.dump(pc)}), 200)


# Update policy coverage
# ===============================================================================
@policy_coverage_bp.route('/api/policy_coverages/<int:pc_id>', methods=['PUT'])
def update_policy_coverage(pc_id):
    """Update an existing policy coverage."""
    pc = PolicyCoverage.query.get_or_404(pc_id)
    data = request.get_json()

    schema = PolicyCoverageSchema()
    updated = schema.load(data, instance=pc, partial=True)

    db.session.commit()
    return make_response(jsonify({
        "message": "Policy coverage updated successfully",
        "policy_coverage": schema.dump(updated)
    }), 200)


# Delete policy coverage
# ===============================================================================
@policy_coverage_bp.route('/api/policy_coverages/<int:pc_id>', methods=['DELETE'])
def delete_policy_coverage(pc_id):
    """Delete a policy coverage."""
    pc = PolicyCoverage.query.get_or_404(pc_id)
    db.session.delete(pc)
    db.session.commit()
    return make_response(jsonify({"message": "Policy coverage deleted successfully"}), 200)
