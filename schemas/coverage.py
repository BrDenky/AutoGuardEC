"""
Coverage schema definition.
"""

from extensions import ma
from models.coverage import Coverage


class CoverageSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Coverage objects."""
    
    class Meta:
        model = Coverage
        include_fk = True
        load_instance = True
