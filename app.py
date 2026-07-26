# server/app.py
from flask import Flask, make_response, jsonify, request
from extensions import db, migrate
from models import Exercise, Workout, WorkoutExercise
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

# WORKOUT ROUTES

# GET /workouts - List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    # TODO: Add serialization in step 10
    return jsonify([{"id": w.id, "date": w.date.isoformat(), "duration_minutes": w.duration_minutes, "notes": w.notes} for w in workouts]), 200

# GET /workouts/<id> - Show a single workout with its associated exercises
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    # TODO: Add serialization and stretch goal (include reps/sets/duration data) in step 10
    return jsonify({
        "id": workout.id, 
        "date": workout.date.isoformat(), 
        "duration_minutes": workout.duration_minutes, 
        "notes": workout.notes
    }), 200

# POST /workouts - Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        # Simple parsing example; handle validation/date formatting as needed
        new_workout = Workout(
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else datetime.utcnow().date(),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"id": new_workout.id, "date": new_workout.date.isoformat()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /workouts/<id> - Delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    # Stretch goal: delete associated WorkoutExercises handled automatically if cascade/relationships are configured, 
    # otherwise can explicitly clear workout_exercises here.
    db.session.delete(workout)
    db.session.commit()
    return '', 204


# EXERCISE ROUTES

# GET /exercises - List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{"id": e.id, "name": e.name, "category": e.category, "equipment_needed": e.equipment_needed} for e in exercises]), 200

# GET /exercises/<id> - Show an exercise and associated workouts
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    }), 200

# POST /exercises - Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify({"id": new_exercise.id, "name": new_exercise.name}), 201
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /exercises/<id> - Delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return '', 204



# WORKOUT_EXERCISES JOIN ROUTE

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add exercise to workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    if not workout or not exercise:
        return jsonify({"error": "Workout or Exercise not found"}), 404
        
    data = request.get_json()
    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify({
            "id": workout_exercise.id,
            "workout_id": workout_exercise.workout_id,
            "exercise_id": workout_exercise.exercise_id,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)