"""
PremiumPayment model definition.
"""

from extensions import db


class PremiumPayment(db.Model):
    """PremiumPayment model representing premium payments for policies."""
    
    __tablename__ = 'PremiumPayment'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    payment_id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'))
    payment_date = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    policy = db.relationship('Policy', back_populates='premium_payments')
