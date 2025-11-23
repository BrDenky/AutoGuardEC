"""
ClaimPayment model definition.
"""

from extensions import db


class ClaimPayment(db.Model):
    """ClaimPayment model representing payments for claims."""
    
    __tablename__ = 'ClaimPayment'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    claim_payment_id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('Claim.claim_id'))
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    claim = db.relationship('Claim', back_populates='claim_payments')
