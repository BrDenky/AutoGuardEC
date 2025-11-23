"""
AutoGuardEC - Car Insurance Management System
Main application entry point using Application Factory pattern.
"""

from flask import Flask
from extensions import db, ma
from config import Config


def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use (default: Config)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    from routes import (
        customer_bp, vehicle_bp, agent_bp, coverage_bp,
        policy_bp, premium_payment_bp, claim_bp, 
        claim_payment_bp, policy_coverage_bp,
        dashboard_bp, frontend_bp
    )
    
    app.register_blueprint(customer_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(coverage_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(premium_payment_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(claim_payment_bp)
    app.register_blueprint(policy_coverage_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(frontend_bp)
    
    # Create database tables
    with app.app_context():
        # Import all models to ensure they're registered with SQLAlchemy
        from models import (
            Customer, Vehicle, Agent, Coverage, Policy,
            PremiumPayment, Claim, ClaimPayment, PolicyCoverage
        )
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)