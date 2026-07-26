# server/app.py
from flask import Flask, jsonify, request
from extensions import db, migrate
from models import Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


# WORKOUT ENDPOINTS

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.jsonify(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return workout_schema.jsonify(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    try:
        data = workout_schema.load(json_data)
        new_workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.jsonify(new_workout), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    # Stretch goal: explicit cleanup or relying on cascade delete-orphan
    for we in workout.workout_exercises:
        db.session.delete(we)
        
    db.session.delete(workout)
    db.session.commit()
    return '', 204


# EXERCISE ENDPOINTS

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.jsonify(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return exercise_schema.jsonify(exercise), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    try:
        data = exercise_schema.load(json_data)
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(new_exercise)
        db.session.commit()
        return exercise_schema.jsonify(new_exercise), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    for we in exercise.workout_exercises:
        db.session.delete(we)
        
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


# WORKOUT_EXERCISES JOIN ENDPOINT

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    if not workout or not exercise:
        return jsonify({"error": "Workout or Exercise not found"}), 404
        
    json_data = request.get_json()
    try:
        data = workout_exercise_schema.load(json_data)
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return workout_exercise_schema.jsonify(workout_exercise), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)