# ===============================================================================
# Vehicle model definition.
# ===============================================================================

from extensions import db

# Vehicle table
# ===============================================================================
class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    
    vehicle_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    license_plate = db.Column(db.String(20), unique=True)

    # Vehicle relationships
    # ===============================================================================
    customer = db.relationship('Customer', back_populates='vehicles')
    policies = db.relationship('Policy', back_populates='vehicle', cascade='all, delete-orphan')
