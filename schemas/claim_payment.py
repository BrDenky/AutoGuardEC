"""
ClaimPayment schema definition.
"""

from extensions import ma
from models.claim_payment import ClaimPayment


class ClaimPaymentSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing ClaimPayment objects."""
    
    class Meta:
        model = ClaimPayment
        include_fk = True
        load_instance = True
