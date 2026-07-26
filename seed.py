#!/usr/bin/env python3

from app import app
from extensions import db
from models import Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    print("Deleting existing data...")
    # Delete in order of dependency (child tables first)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Creating exercises...")
    ex1 = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Barbell Bench Press", category="Strength", equipment_needed=True)
    ex3 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    
    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Creating workouts...")
    w1 = Workout(date=date(2026, 7, 1), duration_minutes=45, notes="Upper body day")
    w2 = Workout(date=date(2026, 7, 3), duration_minutes=30, notes="Cardio endurance")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Linking exercises to workouts (WorkoutExercises)...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, sets=4, reps=8)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex3.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeding completed successfully!")