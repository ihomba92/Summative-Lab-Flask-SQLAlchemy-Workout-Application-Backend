# server/schemas.py
from marshmallow import Schema, fields, validates, ValidationError, validate

class ExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed', 'workout_exercises')
    
    # Schema validation 1: Ensure name is provided, is a string, and not empty/whitespace
    name = fields.Str(required=True, validate=lambda n: bool(n and n.strip()), error_messages={"validator_failed": "Exercise name cannot be empty."})
    category = fields.Str(required=True)
    equipment_needed = fields.Boolean()

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('exercise',))))

    @validates('name')
    def validate_exercise_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty or just whitespace.")


class WorkoutSchema(Schema):
    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes', 'workout_exercises', 'exercises')
    
    # Schema validation 2: Ensure workout duration cannot be negative (mirrors table constraint)
    duration_minutes = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Duration cannot be negative."))
    
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('workout',))))
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises',))))


class WorkoutExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds', 'workout', 'exercise')
    
    # Schema validation 3: Ensure metrics like sets, reps, and duration cannot be negative
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Sets cannot be negative."))
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Reps cannot be negative."))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Duration in seconds cannot be negative."))

    workout = fields.Nested(WorkoutSchema(exclude=('workout_exercises', 'exercises')))
    exercise = fields.Nested(ExerciseSchema(exclude=('workout_exercises',)))