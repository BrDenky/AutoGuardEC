# ===============================================================================
# PolicyCoverage model definition.
# ===============================================================================

from extensions import db

# PolicyCoverage table
# ===============================================================================
class PolicyCoverage(db.Model):
    __tablename__ = 'PolicyCoverage'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    policy_id = db.Column(db.Integer, db.ForeignKey('Policy.policy_id'), primary_key=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('Coverage.coverage_id'), primary_key=True)
