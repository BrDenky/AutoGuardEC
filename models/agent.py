# ===============================================================================
# Agent model definition.
# ===============================================================================

from extensions import db

# Agent table
# ===============================================================================
class Agent(db.Model):
    __tablename__ = 'Agent'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    agent_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    # Agent relationships
    # ===============================================================================
    policies = db.relationship('Policy', back_populates='agent', cascade='all, delete-orphan')
