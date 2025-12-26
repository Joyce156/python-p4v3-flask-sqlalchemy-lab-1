#!/usr/bin/env python3
# server/seed.py

# Remove: from app import app
from models import db, Earthquake

def seed_data():
    from app import app  # Import inside function to avoid circular import
    
    with app.app_context():
        print("Seeding earthquake data...")
        
        # Delete all rows in the "earthquakes" table
        Earthquake.query.delete()

        # Add several Earthquake instances to the "earthquakes" table
        db.session.add(Earthquake(magnitude=9.5, location="Chile", year=1960))
        db.session.add(Earthquake(magnitude=9.2, location="Alaska", year=1964))
        db.session.add(Earthquake(magnitude=8.6, location="Alaska", year=1946))
        db.session.add(Earthquake(magnitude=8.5, location="Banda Sea", year=1934))
        db.session.add(Earthquake(magnitude=8.4, location="Chile", year=1922))

        # Commit the transaction
        db.session.commit()
        print("Seeding complete!")