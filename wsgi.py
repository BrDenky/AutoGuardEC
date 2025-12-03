# ===============================================================================
# WSGI Entry Point for AutoGuardEC - Car Insurance Management System
# ===============================================================================
# This file is used by Gunicorn to load the Flask application

from app import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run()
