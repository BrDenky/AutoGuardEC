# ===============================================================================
# Customer model definition.
# ===============================================================================

from extensions import db

# Customer table
# ===============================================================================
class Customer(db.Model):
    __tablename__ = 'Customer'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)

    # Customer relationships
    # ===============================================================================
    vehicles = db.relationship('Vehicle', back_populates='customer', cascade='all, delete-orphan')
    policies = db.relationship('Policy', back_populates='customer', cascade='all, delete-orphan')
