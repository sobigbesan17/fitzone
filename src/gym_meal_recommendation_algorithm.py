import sqlite3 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score 
 
class GymMealRecommendationAlgorithm: 
    def __init__(self, db_file='FitZone.db'): 
        self.conn = sqlite3.connect(db_file) 
        self.vectorizer = CountVectorizer(analyzer=lambda x: x.split(',')) 
        self.model = RandomForestClassifier(n_estimators=100, random_state=42) 
        self.data = None 
        self.X_train = None 
        self.y_train = None 
    def load_data(self): 
        query = ''' 
            SELECT MealName, MealType, Calories, Protein, Fat, Carbohydrates, 
Ingredients, CookingTime, NutritionalGoals, Budget, DietaryRestrictions, 
Allergies, MealSize 
            FROM Meals 
            UNION ALL 
            SELECT MealName, MealType, Calories, Protein, Fat, Carbohydrates, 
Ingredients, CookingTime, NutritionalGoals, Budget, DietaryRestrictions, 
Allergies, MealSize 
            FROM CustomMeals 
        ''' 
        self.data = pd.read_sql_query(query, self.conn) 
 
    def preprocess_data(self): 
        X = self.data.drop('MealName', axis=1) 
        y = self.data['MealName'] 
        self.X_train, _, self.y_train, _ = train_test_split(X, y, test_size=0.2, 
random_state=42) 
 
        self.X_train['MealType'] = self.X_train['MealType'].apply(lambda x: 
','.join(x.split(','))) 
        self.X_train['Ingredients'] = self.X_train['Ingredients'].apply(lambda 
x: ','.join(x.split(','))) 
 
        self.X_train = pd.get_dummies(self.X_train, columns=['MealType'], 
prefix=['MealType']) 
        self.X_train = self.vectorizer.fit_transform(self.X_train['Ingredients']) 
        self.model.fit(self.X_train, self.y_train) 
 
    def get_recommendation(self, user_input): 
        user_input['MealType'] = ','.join(user_input['MealType'].split(',')) 
        user_input['Ingredients'] = ','.join(user_input['Ingredients'].split(',')) 
        user_input_encoded = self.vectorizer.transform([user_input['Ingredients']]) 
        recommended_meals = self.model.predict(user_input_encoded) 
         
        numerical_weight = 0.6 
        ingredients_weight = 0.4 
        best_recommendation = None 
        best_similarity_score = float('inf') 
 
        recommended_meal_details = self.data[self.data['MealName'].isin(recommended_meals)] 
        if recommended_meal_details.empty: 
            return "No meaningful recommendations found."

        for index in recommended_meal_details.index: 
            row = recommended_meal_details.loc[index] 
            numerical_score = 0 
 
            for factor in ['Budget', 'Calories', 'Carbohydrates', 'Protein', 
'Fat', 'CookingTime', 'MealSize']:  
                try: 
                    numerical_score += numerical_weight * abs(float(row[factor]) - float(user_input[factor])) 
                except (ValueError, TypeError): 
                    print("Error: Unable to perform subtraction or convert data for factor:", factor) 
 
            ingredients_similarity_score = ingredients_weight * self.calculate_ingredients_similarity(user_input['Ingredients'], row['Ingredients']) 
 
            combined_score = numerical_score + ingredients_similarity_score 
 
            if combined_score < best_similarity_score: 
                best_similarity_score = combined_score 
                best_recommendation = row['MealName'] 
 
        return f"Recommended Meal: {best_recommendation}" 
 
    def calculate_ingredients_similarity(self, input_ingredients, 
meal_ingredients): 
        input_set = set(input_ingredients.split(',')) 
        meal_set = set(meal_ingredients.split(',')) 
        intersection = len(input_set.intersection(meal_set)) 
        union = len(input_set.union(meal_set)) 
        similarity_score = intersection / union if union > 0 else 0 
        return similarity_score 
