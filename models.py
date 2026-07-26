from extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # An Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    # Model Validation: Ensure exercise name is not empty or whitespace
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Table Constraint 1: Ensure workout duration cannot be negative
    __table_args__ = (
        CheckConstraint('duration_minutes >= 0', name='check_duration_minutes_non_negative'),
    )

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # A Workout has many Exercises through WorkoutExercises
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Table Constraint 2: Prevent duplicate exercises in the same workout
    __table_args__ = (
        UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
    )

    # A WorkoutExercise belongs to a Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')
    
    # A WorkoutExercise belongs to an Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model Validation 2: Ensure sets, reps, and duration cannot be negative
    @validates('sets', 'reps', 'duration_seconds')
    def validate_positive_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value