"""
Claim model definition.
"""

from extensions import db


class Claim(db.Model):
    """Claim model representing insurance claims."""
    
    __tablename__ = 'Claim'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    claim_id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'))
    claim_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('open', 'closed', 'in review'))

    # Relationships
    policy = db.relationship('Policy', back_populates='claims')
    claim_payments = db.relationship('ClaimPayment', back_populates='claim', cascade='all, delete-orphan')
