# Flask SQLAlchemy Workout Application (Backend)

A fully-featured backend REST API built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow. This application manages workouts, exercises, and their junction relationships with robust data validation and serialization.

---

## Features

* **Relational Database Architecture**: Models for `Workout`, `Exercise`, and a join table `WorkoutExercise` implementing many-to-many relationships.
* **Data Validation & Constraints**: 
  * Model-level and schema-level validations ensuring non-negative metrics (sets, reps, duration) and non-empty exercise names.
  * Unique and check constraints configured at the table level.
* **Marshmallow Serialization**: Clean input deserialization (`.load()`) and output serialization (`.jsonify()`) with nested relationship mapping and prevention of recursive loops.
* **RESTful Endpoints**: Full CRUD support for workouts, exercises, and adding exercises to specific workouts.

---

## Tech Stack

* **Python** (v3.12+)
* **Flask** (v2.2.2)
* **Flask-SQLAlchemy** (v3.0.3)
* **Flask-Migrate** (v3.1.0)
* **Marshmallow** (v3.20.1)
* **SQLite** (Database)

---

## Project Structure

```text
├── server/
    ├── app.py          # Application factory & route definitions
    ├── models.py       # SQLAlchemy database models & table constraints
    ├── schemas.py      # Marshmallow validation & serialization schemas
    ├── extensions.py   # Shared extensions (db, migrate)
    ├── seed.py         # Database seeding script
    └── app.db          # SQLite database (generated locally)

Getting Started & Installation
1. Clone the Repository
Bash
git clone <your-repository-url>
cd Flask-SQLAlchemy-Workout-Application-Backend/server
#2. Install Dependencies
This project uses Pipenv for dependency management.
Bash
pipenv install
#3. Activate the Virtual Environment
Bash
pipenv shell

#4. Initialize the Database & Run Migrations
Bash
export FLASK_APP=app.py
pipenv run flask db init
pipenv run flask db migrate -m "initial migration"
pipenv run flask db upgrade
#5. Seed the Database
Populate the database with initial mock data:
Bash
pipenv run python seed.py
#6. Run the Application
Start the development server:

Bash
python app.py
The server will run locally at http://localhost:5555.

##API Endpoints Reference
#Workouts
GET /workouts - Retrieve a list of all workouts.

GET /workouts/<id> - Retrieve a single workout along with its associated exercises.

POST /workouts - Create a new workout.

DELETE /workouts/<id> - Delete a workout and its associated join relations.

#Exercises
GET /exercises - Retrieve a list of all exercises.

GET /exercises/<id> - Retrieve a single exercise along with associated workouts.

POST /exercises - Create a new exercise.

DELETE /exercises/<id> - Delete an exercise.

##Workout Exercises (Join Route)
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add an exercise to a specific workout with custom sets, reps, or duration metrics.