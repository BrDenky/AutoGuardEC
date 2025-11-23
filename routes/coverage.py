"""
Coverage routes blueprint.
"""

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.coverage import Coverage
from schemas.coverage import CoverageSchema

coverage_bp = Blueprint('coverages', __name__)


@coverage_bp.route('/api/coverages/', methods=['GET'])
def get_coverages():
    """Get all coverages with pagination."""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    coverages_paginated = Coverage.query.paginate(page=page, per_page=limit, error_out=False)

    schema = CoverageSchema(many=True)
    result = schema.dump(coverages_paginated.items)

    response = {
        "coverages": result,
        "total_coverages": coverages_paginated.total,
        "total_pages": coverages_paginated.pages,
        "current_page": coverages_paginated.page,
        "has_next": coverages_paginated.has_next,
        "has_prev": coverages_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


@coverage_bp.route('/api/coverages/<int:coverage_id>', methods=['GET'])
def get_coverage(coverage_id):
    """Get a specific coverage by ID."""
    coverage = Coverage.query.get_or_404(coverage_id)
    coverage_schema = CoverageSchema()
    result = coverage_schema.dump(coverage)
    return make_response(jsonify({"coverage": result}), 200)


@coverage_bp.route('/api/coverages/<int:coverage_id>', methods=['PUT'])
def update_coverage(coverage_id):
    """Update an existing coverage."""
    coverage = Coverage.query.get_or_404(coverage_id)
    data = request.get_json()

    coverage_schema = CoverageSchema()
    updated_coverage = coverage_schema.load(data, instance=coverage, partial=True)

    db.session.commit()
    result = coverage_schema.dump(updated_coverage)

    return make_response(jsonify({'message': 'Coverage updated successfully', 'coverage': result}), 200)


@coverage_bp.route('/api/coverages/<int:coverage_id>', methods=['DELETE'])
def delete_coverage(coverage_id):
    """Delete a coverage."""
    coverage = Coverage.query.get_or_404(coverage_id)
    db.session.delete(coverage)
    db.session.commit()
    return make_response(jsonify({'message': 'Coverage deleted successfully'}), 200)
