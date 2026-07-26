# server/app.py
from flask import Flask, make_response
from extensions import db, migrate
from models import Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

# Define Routes here

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    