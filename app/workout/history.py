from app.models import Workout

def get_history_list(current_user):
    user_id = current_user.id
    workouts = Workout.query.filter_by(user_id=user_id)
    return workouts

