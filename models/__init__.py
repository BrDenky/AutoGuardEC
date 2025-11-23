"""
Models package initialization.
Imports all models to make them available for SQLAlchemy.
"""

from models.customer import Customer
from models.vehicle import Vehicle
from models.agent import Agent
from models.coverage import Coverage
from models.policy import Policy
from models.premium_payment import PremiumPayment
from models.claim import Claim
from models.claim_payment import ClaimPayment
from models.policy_coverage import PolicyCoverage

__all__ = [
    'Customer',
    'Vehicle',
    'Agent',
    'Coverage',
    'Policy',
    'PremiumPayment',
    'Claim',
    'ClaimPayment',
    'PolicyCoverage'
]
