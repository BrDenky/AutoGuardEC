"""
Shared extensions for the Flask application.
This module prevents circular imports by centralizing extension instances.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
