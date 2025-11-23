"""
Vehicle schema definition.
"""

from extensions import ma
from models.vehicle import Vehicle


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Vehicle objects."""
    
    class Meta:
        model = Vehicle
        include_fk = True
        load_instance = True
