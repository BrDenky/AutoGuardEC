# ===============================================================================
# Dashboard routes blueprints
# ===============================================================================

from flask import Blueprint, jsonify
from extensions import db
from models.customer import Customer
from models.vehicle import Vehicle
from models.policy import Policy
from models.agent import Agent

dashboard_bp = Blueprint('dashboard', __name__)


# Get dashboard statistics
# ===============================================================================
@dashboard_bp.route('/api/dashboard-data')
def dashboard_data():
    """Get dashboard statistics."""
    stats = get_dashboard_stats()
    return jsonify(stats)

# Statistics calculation
# ===============================================================================
def get_dashboard_stats():
    stats = {
        'total_customers': db.session.query(Customer).count(),
        'total_vehicles': db.session.query(Vehicle).count(),
        'active_policies': db.session.query(Policy).filter(Policy.status == 'active').count(),
        'expired_policies': db.session.query(Policy).filter(Policy.status == 'expired').count(),
        'canceled_policies': db.session.query(Policy).filter(Policy.status == 'canceled').count(),
        'total_agents': db.session.query(Agent).count(),
    }
    
    return stats
