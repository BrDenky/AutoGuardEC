"""
PolicyCoverage schema definition.
"""

from extensions import ma
from models.policy_coverage import PolicyCoverage


class PolicyCoverageSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing/deserializing PolicyCoverage objects."""
    
    class Meta:
        model = PolicyCoverage
        include_fk = True
        load_instance = True
