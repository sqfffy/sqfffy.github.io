from app import app, db  # Import your app module

with app.app_context():
    db.create_all()  # This creates the database tables
