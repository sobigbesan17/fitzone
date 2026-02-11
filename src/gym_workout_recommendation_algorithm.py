import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

class GymWorkoutRecommendationAlgorithm:
    def __init__(self, db_file='FitZone.db'):
        self.conn = sqlite3.connect(db_file)
        self.vectorizer = CountVectorizer(analyzer=lambda x: x.split(','))
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.data = None
        self.X_train = None
        self.y_train = None

    def load_data(self):
        query = '''
            SELECT WorkoutName, WorkoutType, Duration, Intensity, Equipment,
                   TargetMuscles, FitnessGoal, ExperienceLevel
            FROM Workouts
            UNION ALL
            SELECT WorkoutName, WorkoutType, Duration, Intensity, Equipment,
                   TargetMuscles, FitnessGoal, ExperienceLevel
            FROM CustomWorkouts
        '''
        self.data = pd.read_sql_query(query, self.conn)

    def preprocess_data(self):
        X = self.data.drop('WorkoutName', axis=1)
        y = self.data['WorkoutName']
        self.X_train, _, self.y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        self.X_train['WorkoutType'] = self.X_train['WorkoutType'].apply(lambda x: ','.join(x.split(',')))
        self.X_train['TargetMuscles'] = self.X_train['TargetMuscles'].apply(lambda x: ','.join(x.split(',')))
        self.X_train = pd.get_dummies(self.X_train, columns=['WorkoutType'], prefix=['WorkoutType'])
        self.X_train = self.vectorizer.fit_transform(self.X_train['TargetMuscles'])
        self.model.fit(self.X_train, self.y_train)

    def get_recommendation(self, user_input):
        user_input['WorkoutType'] = ','.join(user_input['WorkoutType'].split(','))
        user_input['TargetMuscles'] = ','.join(user_input['TargetMuscles'].split(','))
        user_encoded = self.vectorizer.transform([user_input['TargetMuscles']])
        predicted = self.model.predict(user_encoded)
        numerical_weight = 0.6
        muscle_weight = 0.4
        best = None
        best_score = float('inf')
        details = self.data[self.data['WorkoutName'].isin(predicted)]
        if details.empty:
            return "No meaningful workout recommendations found."
        for index in details.index:
            row = details.loc[index]
            numerical_score = 0
            for factor in ['Duration', 'Intensity', 'ExperienceLevel']:
                try:
                    numerical_score += numerical_weight * abs(float(row[factor]) - float(user_input[factor]))
                except:
                    pass
            muscle_similarity = muscle_weight * self.calculate_muscle_similarity(user_input['TargetMuscles'], row['TargetMuscles'])
            score = numerical_score + muscle_similarity
            if score < best_score:
                best_score = score
                best = row['WorkoutName']
        return f"Recommended Workout: {best}"

    def calculate_muscle_similarity(self, input_muscles, workout_muscles):
        input_set = set(input_muscles.split(','))
        workout_set = set(workout_muscles.split(','))
        intersection = len(input_set.intersection(workout_set))
        union = len(input_set.union(workout_set))
        return intersection / union if union > 0 else 0
