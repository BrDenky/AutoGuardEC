"""
Frontend routes blueprint.
"""

from flask import Blueprint, render_template
from routes.dashboard import get_dashboard_stats

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def home():
    """Render home page with dashboard statistics."""
    stats = get_dashboard_stats()
    return render_template('index.html', 
                         title="Car Insurance System",
                         **stats)


@frontend_bp.route('/customers')
def customers_view():
    """Render customers page."""
    return render_template('customers.html', title="Customers")


@frontend_bp.route('/vehicles')
def vehicles_view():
    """Render vehicles page."""
    return render_template('vehicles.html', title="Vehicles")


@frontend_bp.route('/policies')
def policies_view():
    """Render policies page."""
    return render_template('policies.html', title="Policies")


@frontend_bp.route('/agents')
def agents_view():
    """Render agents page."""
    return render_template('agents.html', title="Agents")


@frontend_bp.route('/coverages')
def coverages_view():
    """Render coverages page."""
    return render_template('coverages.html', title="Coverages")


@frontend_bp.route('/premium_payments')
def premium_payments_view():
    """Render premium payments page."""
    return render_template('premiumpayments.html', title="Premium_Payments")


@frontend_bp.route('/claims')
def claims_view():
    """Render claims page."""
    return render_template('claims.html', title="Claims")


@frontend_bp.route('/claim_payment')
def claim_payments_view():
    """Render claim payments page."""
    return render_template('claimpayments.html', title="Claim_Payment")


@frontend_bp.route('/policy_coverages')
def policy_coverages_view():
    """Render policy coverages page."""
    return render_template('policycoverages.html', title="Policy_Coverages")
