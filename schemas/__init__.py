"""
Schemas package initialization.
Imports all schemas to make them available.
"""

from schemas.customer import CustomerSchema
from schemas.vehicle import VehicleSchema
from schemas.agent import AgentSchema
from schemas.coverage import CoverageSchema
from schemas.policy import PolicySchema
from schemas.premium_payment import PremiumPaymentSchema
from schemas.claim import ClaimSchema
from schemas.claim_payment import ClaimPaymentSchema
from schemas.policy_coverage import PolicyCoverageSchema

__all__ = [
    'CustomerSchema',
    'VehicleSchema',
    'AgentSchema',
    'CoverageSchema',
    'PolicySchema',
    'PremiumPaymentSchema',
    'ClaimSchema',
    'ClaimPaymentSchema',
    'PolicyCoverageSchema'
]
