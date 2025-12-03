# ===============================================================================
# ROUTES AutoGuardEC - Car Insurance Management System
# Import blueprints to make them available
# ===============================================================================

from routes.customer import customer_bp
from routes.vehicle import vehicle_bp
from routes.agent import agent_bp
from routes.coverage import coverage_bp
from routes.policy import policy_bp
from routes.premium_payment import premium_payment_bp
from routes.claim import claim_bp
from routes.claim_payment import claim_payment_bp
from routes.policy_coverage import policy_coverage_bp
from routes.dashboard import dashboard_bp
from routes.frontend import frontend_bp
from routes.customer_profile_pdf import customer_profile_pdf_bp

__all__ = [
    'customer_bp',
    'vehicle_bp',
    'agent_bp',
    'coverage_bp',
    'policy_bp',
    'premium_payment_bp',
    'claim_bp',
    'claim_payment_bp',
    'policy_coverage_bp',
    'dashboard_bp',
    'frontend_bp',
    'customer_profile_pdf_bp'
]
