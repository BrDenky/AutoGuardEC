"""
Claim schema definition.
"""

from extensions import ma
from models.claim import Claim


class ClaimSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Claim objects."""
    
    class Meta:
        model = Claim
        include_fk = True
        load_instance = True
