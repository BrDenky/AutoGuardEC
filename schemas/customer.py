"""
Customer schema definition.
"""

from extensions import ma
from models.customer import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Customer objects."""
    
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True

