from os import abort

from app.workout import history
from app.constants.exercises import abs, arms, back, cardio, chest, legs, shoulders

class Workout_Manager:
    user_id = None

    def __init__(self, user_id):
        self.user_id = user_id

    def create_workout(self):
        return False

    def get_workouts(self):
        workouts = history.get_history_list(self.user_id)
        return workouts

    def get_exercises(self, category):
        if category == 'Abs':
            return abs.workout_exercises
        elif category == 'Arms':
            return arms.workout_exercises
        elif category == 'Back':
            return back.workout_exercises
        elif category == 'Cardio':
            return cardio.workout_exercises
        elif category == 'Chest':
            return chest.workout_exercises
        elif category == 'Legs':
            return legs.workout_exercises
        elif category == 'Shoulders':
            return shoulders.workout_exercises
        else:
            return 'Category not found', 404

class Workout:
    user = None
    date_posted = None
    category = None
    exercises = []

    def __init__(self, user, date_posted, category):
        self.user = user
        self.date_posted = date_posted
        self.category = category

    def add_exercise(self, exercise, sets, reps, weight):
        exercise = {
            'exercise': exercise,
            'sets': sets,
            'reps': reps,
            'weight': weight
        }

        self.exercises.append(exercise)

    def get_workout(self):
        return {
            'user': self.user.id,
            'date_posted': self.date_posted,
            'category': self.category,
            'exercises': self.exercises
        }
