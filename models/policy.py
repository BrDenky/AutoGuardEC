"""
Policy model definition.
"""

from extensions import db


class Policy(db.Model):
    """Policy model representing insurance policies."""
    
    __tablename__ = 'Policy'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    
    policy_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.vehicle_id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('Agent.agent_id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('active', 'expired', 'canceled', 'arrears'))

    # Relationships
    customer = db.relationship('Customer', back_populates='policies')
    vehicle = db.relationship('Vehicle', back_populates='policies')
    agent = db.relationship('Agent', back_populates='policies')
    coverages = db.relationship('Coverage', secondary='PolicyCoverage', back_populates='policies')
    claims = db.relationship('Claim', back_populates='policy', cascade='all, delete-orphan')
    premium_payments = db.relationship('PremiumPayment', back_populates='policy', cascade='all, delete-orphan')
