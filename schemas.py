# server/schemas.py
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date

class ExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed', 'workout_exercises')
    
    name = fields.Str(required=True, validate=lambda n: bool(n and n.strip()))
    category = fields.Str(required=True)
    equipment_needed = fields.Boolean(load_default=False)

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('exercise',))), dump_only=True)

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty.")


class WorkoutSchema(Schema):
    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes', 'workout_exercises', 'exercises')
    
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Duration cannot be negative."))
    notes = fields.Str(allow_none=True)
    
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('workout',))), dump_only=True)
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises',))), dump_only=True)


class WorkoutExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds', 'workout', 'exercise')
    
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Sets cannot be negative."))
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Reps cannot be negative."))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="Duration in seconds cannot be negative."))

    workout = fields.Nested(WorkoutSchema(exclude=('workout_exercises', 'exercises')), dump_only=True)
    exercise = fields.Nested(ExerciseSchema(exclude=('workout_exercises',)), dump_only=True)