"""
Policy schema definition.
"""

from extensions import ma
from models.policy import Policy


class PolicySchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Policy objects."""
    
    class Meta:
        model = Policy
        include_fk = True
        load_instance = True
