#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ✅ REQUIRED so pytest has tables
with app.app_context():
    db.create_all()
    # Seed data if table is empty
    if Earthquake.query.count() == 0:
        from seed import seed_data  # Import here to avoid circular import
        seed_data()


@app.route('/')
def index():
    return make_response(
        {"message": "Flask SQLAlchemy Lab 1"},
        200
    )


# ✅ Task 3: Get earthquake by id
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if quake is None:
        return make_response(
            {"message": f"Earthquake {id} not found."},
            404
        )

    return make_response(
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        },
        200
    )


# ✅ Task 4: Get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return make_response(
        {
            "count": len(quakes),
            "quakes": [
                {
                    "id": q.id,
                    "location": q.location,
                    "magnitude": q.magnitude,
                    "year": q.year
                }
                for q in quakes
            ]
        },
        200
    )


if __name__ == '__main__':
    app.run(port=5555, debug=True)