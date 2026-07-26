# server/schemas.py
from marshmallow import Schema, fields, validates, ValidationError

class ExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed', 'workout_exercises')
    
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('exercise',))))

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty.")


class WorkoutSchema(Schema):
    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes', 'workout_exercises', 'exercises')
    
    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('workout',))))
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises',))))


class WorkoutExerciseSchema(Schema):
    class Meta:
        fields = ('id', 'workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds', 'workout', 'exercise')
    
    workout = fields.Nested(WorkoutSchema(exclude=('workout_exercises', 'exercises')))
    exercise = fields.Nested(ExerciseSchema(exclude=('workout_exercises',)))