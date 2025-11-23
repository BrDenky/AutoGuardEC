"""
PremiumPayment schema definition.
"""

from extensions import ma
from models.premium_payment import PremiumPayment


class PremiumPaymentSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing PremiumPayment objects."""
    
    class Meta:
        model = PremiumPayment
        include_fk = True
        load_instance = True
