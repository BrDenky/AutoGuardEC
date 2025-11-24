# ===============================================================================
# Coverage model definition.
# ===============================================================================

from extensions import db

# Coverage table
# ===============================================================================
class Coverage(db.Model):
    __tablename__ = 'Coverage'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    coverage_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Coverage relationships
    # ===============================================================================
    policies = db.relationship('Policy', secondary='PolicyCoverage', back_populates='coverages')
