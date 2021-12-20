from app.models import Workout

def get_history_list(user_id):
    workouts = []
    results = Workout.query.filter_by(user_id=user_id)

    try:
        for workout in results:
            workouts.append(workout)
    except Exception as e:
        print('Error: ' + str(e))

    return workouts

