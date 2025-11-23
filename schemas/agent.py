"""
Agent schema definition.
"""

from extensions import ma
from models.agent import Agent


class AgentSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing Agent objects."""
    
    class Meta:
        model = Agent
        include_fk = True
        load_instance = True
