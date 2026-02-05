import os 
import sqlite3 
from sample_meal_data import *
from sample_workout_data import * 
from sample_exercise_data import * 
 
def delete_file(file_path): 
    if os.path.exists(file_path): 
        try: 
            os.remove(file_path) 
            print(f"{file_path} deleted successfully.") 
        except Exception as e: 
            print("Error occurred:", e) 
    else: 
        print("Database does not exist.") 
 
# Creates all the SQL tables 
def create_all_tables(): 
    try: 
        conn = sqlite3.connect('FitZone.db') 
        cursor = conn.cursor() 
 
        # Create the GymLocations table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymLocations ( 
                LocationID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationName VARCHAR(100) NOT NULL, 
                Address VARCHAR(200), 
                EmailAddress VARCHAR(100), 
                ContactNumber VARCHAR(20) 
            ); 
        ''') 
 
        # Create the TeamLeaders table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS TeamLeaders ( 
                LeaderID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LeaderName VARCHAR(100) NOT NULL, 
                RoleDescription VARCHAR(200), 
                ImagePath VARCHAR(200), 
                LocationID INTEGER, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the Studios table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymStudios ( 
                StudioID INTEGER PRIMARY KEY AUTOINCREMENT, 
                StudioName VARCHAR(100) NOT NULL, 
                Capacity INTEGER, 
                LocationID INTEGER, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations (LocationID) 
            ); 
        ''') 
 
        # Create the GymBenefits table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymBenefits ( 
                GymBenefitID INTEGER PRIMARY KEY AUTOINCREMENT, 
                BenefitName TEXT, 
                LocationID INTEGER, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ) 
        ''') 
 
        # Create the GymReview table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymReview ( 
                ReviewID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                ReviewerID INTEGER, 
                ReviewName TEXT, 
                ReviewText TEXT, 
                Rating INTEGER, 
                Date DATE, 
                FOREIGN KEY (LocationID) REFERENCES GymLocationsTbl 
(LocationID), 
                FOREIGN KEY (ReviewerID) REFERENCES Members (MemberID) 
            ) 
        ''') 
 
        # Create the GymReview reply table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymReply ( 
                ReplyID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ReviewID INTEGER, 
                ReplyText TEXT, 
                ReplyDate DATE, 
                FOREIGN KEY (ReviewID) REFERENCES GymReview (ReviewID) 
            ) 
        ''')

 
        # Create the ClassReview table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ClassReview ( 
                ReviewID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ClassID INTEGER, 
                ReviewerID INTEGER, 
                ReviewName TEXT, 
                ReviewText TEXT, 
                Rating INTEGER, 
                Date DATE, 
                FOREIGN KEY (ClassID) REFERENCES GymClasses (ClassID), 
                FOREIGN KEY (ReviewerID) REFERENCES Members (MemberID) 
            ) 
        ''') 
 
        # Create the GymReview reply table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ClassReply ( 
                ReplyID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ReviewID INTEGER, 
                ReplyText TEXT, 
                ReplyDate DATE, 
                FOREIGN KEY (ReviewID) REFERENCES Instructor (InstructorID) 
            ) 
        ''') 
 
 
        # Create the FAQs table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS FAQs ( 
                FAQID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER NOT NULL, 
                Question TEXT NOT NULL, 
                Answer TEXT NOT NULL, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
         
        # Create the GymAmenities table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymAmenities ( 
                AmenityID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                AmenityName VARCHAR(50),
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the GymEquipments table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymEquipments ( 
                EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                EquipmentName VARCHAR(50), 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the OpeningHours table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS OpeningHours ( 
                OpeningHoursID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                Weekday VARCHAR(20), 
                StartTime TIME, 
                EndTime TIME, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
         
        # Create the GymFeatures table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymFeatures ( 
                FeatureID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                FeatureName VARCHAR(50), 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the Members table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Members ( 
                MemberID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                DurationID INTEGER, 
                PackageID INTEGER, 
                Username VARCHAR(50) NOT NULL, 
                Password VARCHAR(100) NOT NULL,
                Salt VARCHAR(100) NOT NULL, 
                Gender VARCHAR(10), 
                Email VARCHAR(100) NOT NULL, 
                DateOfBirth DATE, 
                JoinDate DATE, 
                FirstName VARCHAR(50), 
                LastName VARCHAR(50), 
                Address VARCHAR(200), 
                CountryCode VARCHAR(5), 
                PhoneNumber VARCHAR(20), 
                ImagePath VARCHAR(200), 
                EmailNotifications BOOLEAN, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
                FOREIGN KEY (PackageID) REFERENCES MembershipPackages 
(PackageID) 
                FOREIGN KEY (DurationID) REFERENCES MembershipDurations 
(DurationID) 
            ); 
        ''') 
 
        # Create the Testimonials table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Testimonials ( 
                TestimonialID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MemberID INTEGER, 
                TestimonialText TEXT, 
                TestimonialDate DATE, 
                ImagePath VARCHAR(200), 
                FrameColor VARCHAR(20), 
                NameColor VARCHAR(20), 
                TestimonialColor VARCHAR(20), 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID) 
            ); 
        ''') 
 
         # Create the MembershipPackagesFeatures table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MembershipPackagesFeatures ( 
                PackageFeatureID INTEGER PRIMARY KEY AUTOINCREMENT, 
                PackageID INTEGER, 
                FeatureName VARCHAR(100) NOT NULL, 
                IsIncluded BOOLEAN NOT NULL, 
                FOREIGN KEY (PackageID) REFERENCES MembershipPackages(PackageID) 
            ); 
        ''') 
 
        # Create the MembershipPackages table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MembershipPackages ( 
                PackageID INTEGER PRIMARY KEY AUTOINCREMENT, 
                LocationID INTEGER, 
                PackageName VARCHAR(100) NOT NULL, 
                Description TEXT, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the MembershipDurations table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MembershipDurations ( 
                DurationID INTEGER PRIMARY KEY AUTOINCREMENT, 
                DurationName VARCHAR(100) NOT NULL,  
                Description TEXT, 
                NumberOfDays INTEGER, 
                LocationID INTEGER, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the MembershipPrices table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MembershipPrices ( 
                PriceID INTEGER PRIMARY KEY AUTOINCREMENT, 
                DurationID INTEGER, 
                PackageID INTEGER, 
                Price DECIMAL(10, 2) NOT NULL, 
                FOREIGN KEY (DurationID) REFERENCES 
MembershipDurations(DurationID), 
                FOREIGN KEY (PackageID) REFERENCES MembershipPackages(PackageID) 
            ); 
        ''') 
 
        # Create the DailyPrices table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS DailyPrices ( 
                DailyPriceID INTEGER PRIMARY KEY AUTOINCREMENT, 
                NumberOfDays INTEGER, 
                Price DECIMAL(10, 2), 
                LocationID INTEGER, 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID)
            ); 
        ''') 
 
        # Create the Instructors table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Instructors ( 
                InstructorID INTEGER PRIMARY KEY AUTOINCREMENT, 
                InstructorName TEXT, 
                ImagePath VARCHAR(200), 
                LocationID INTEGER,  
                FOREIGN KEY (LocationID) REFERENCES GymLocations (LocationID) 
            ) 
        ''') 
 
        # Create the Staff table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Staff ( 
                StaffID INTEGER PRIMARY KEY AUTOINCREMENT, 
                StaffName VARCHAR(100) NOT NULL, 
                RoleDescription VARCHAR(200), 
                LocationID INTEGER, 
                Gender VARCHAR(10), 
                Email VARCHAR(100) NOT NULL, 
                DateOfBirth DATE, 
                JoinDate DATE, 
                FirstName VARCHAR(50), 
                LastName VARCHAR(50), 
                Address VARCHAR(200), 
                PhoneNumber VARCHAR(20), 
                ImagePath VARCHAR(200), 
                FOREIGN KEY (LocationID) REFERENCES GymLocations(LocationID) 
            ); 
        ''') 
 
        # Create the GymClasses table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS GymClasses ( 
                ClassID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ClassName TEXT, 
                AvailableSlots INTEGER, 
                InstructorID INTEGER, 
                StudioID INTEGER, 
                FOREIGN KEY (InstructorID) REFERENCES Instructors (InstructorID) 
                FOREIGN KEY (StudioID) REFERENCES GymStudios (StudioID) 
            ) 
        ''') 
         
        # Create the Enrollment table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Enrollment ( 
                EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MemberID INTEGER, 
                ClassID INTEGER, 
                FOREIGN KEY (MemberID) REFERENCES Members (MemberID), 
                FOREIGN KEY (ClassID) REFERENCES GymClasses (ClassID) 
            ) 
        ''') 
 
        # Create the Class Schedule table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ClassSchedule ( 
                ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ClassID INTEGER, 
                StartTime TIME, 
                Date DATE, 
                Duration TIME, 
                Message TEXT, 
                FOREIGN KEY (ClassID) REFERENCES GymClasses (ClassID) 
            ) 
        ''') 
 
        # Create the Meal Schedule table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MealSchedule ( 
                MealScheduleID INTEGER PRIMARY KEY AUTOINCREMENT, 
                Date TEXT, 
                Time TEXT, 
                MealID INTEGER, 
                CustomMealID INTEGER, 
                MemberID INTEGER, 
                FOREIGN KEY (MealID) REFERENCES Meals (MealID), 
                FOREIGN KEY (CustomMealID) REFERENCES CustomMeals(CustomMealID), 
                FOREIGN KEY (MemberID) REFERENCES Members (MemberID) 
            ) 
        ''') 
 
        # Create the Meals table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Meals ( 
                MealID INTEGER PRIMARY KEY AUTOINCREMENT,
                MealName TEXT, 
                MealType TEXT, 
                Summary TEXT, 
                Calories INTEGER, 
                Protein REAL, 
                Fat REAL, 
                Carbohydrates REAL, 
                Ingredients TEXT, 
                CookingTime INTEGER, 
                ImagePath VARCHAR(200), 
                MealScheduleID INTEGER NULL, 
                FilePath TEXT, 
                NutritionalGoals TEXT, 
                Budget REAL, 
                DietaryRestrictions TEXT, 
                Allergies TEXT, 
                MealSize INTEGER 
            ) 
        ''')   
 
        # Create the MealReviews table  
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS MealReviews ( 
                ReviewID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MemberID INTEGER, 
                MealID INTEGER, 
                Rating INTEGER, 
                Title VARCHAR(200), 
                Comment TEXT, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID), 
                FOREIGN KEY (MealID) REFERENCES Meals(MealID) 
            ) 
        ''') 
 
        # Create the Custom Meals table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS CustomMeals ( 
                CustomMealID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MealName TEXT, 
                MealType TEXT, 
                Summary TEXT, 
                Calories INTEGER, 
                Protein REAL, 
                Fat REAL, 
                Carbohydrates REAL,'
                Ingredients TEXT, 
                CookingTime INTEGER, 
                ImagePath VARCHAR(200), 
                FilePath TEXT, 
                NutritionalGoals TEXT, 
                Budget REAL, 
                DietaryRestrictions TEXT, 
                Allergies TEXT, 
                MealSize INTEGER, 
                MemberID INTEGER, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID) 
            ) 
        ''') 
 
        # Create the Workouts table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Workouts ( 
                WorkoutID INTEGER PRIMARY KEY AUTOINCREMENT, 
                WorkoutName TEXT, 
                WorkoutType TEXT, 
                WorkoutGoal TEXT, 
                Description TEXT, 
                Difficulty TEXT, 
                ImagePath TEXT, 
                Equipment TEXT, 
                WarmupDuration INT, 
                CooldownDuration INT, 
                WorkoutPlanID INTEGER NULL, 
                WorkoutScheduleID INTEGER NULL, 
                MemberID INTEGER, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID) 
            ) 
        ''') 
 
 
        # Create the Exercises table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Exercises ( 
                ExerciseID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ExerciseName TEXT, 
                ExerciseType TEXT, 
                Description TEXT, 
                Difficulty TEXT, 
                TargetedBodyPart TEXT, 
                Duration INTEGER,
                ImagePath VARCHAR(200) 
            ) 
        ''') 
 
        # Create the WorkoutExercises linking table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS WorkoutExercises ( 
                WorkoutExerciseID INTEGER PRIMARY KEY AUTOINCREMENT, 
                WorkoutID INTEGER, 
                ExerciseID INTEGER, 
                FOREIGN KEY (WorkoutID) REFERENCES Workouts(WorkoutID), 
                FOREIGN KEY (ExerciseID) REFERENCES Exercises(ExerciseID) 
            ) 
        ''') 
 
        # Create the WorkoutReviews table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS WorkoutReviews ( 
                ReviewID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MemberID INTEGER, 
                WorkoutID INTEGER, 
                Rating INTEGER, 
                Title VARCHAR(200), 
                Comment TEXT, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID), 
                FOREIGN KEY (WorkoutID) REFERENCES Workouts(WorkoutID) 
            ) 
        ''') 
 
        # Create the WorkoutSchedules table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS WorkoutSchedules ( 
                ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT, 
                MemberID INTEGER, 
                WorkoutID INTEGER, 
                ScheduledDate DATE, 
                ScheduledTime TIME, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID), 
                FOREIGN KEY (WorkoutID) REFERENCES Workouts(WorkoutID) 
            ) 
        ''') 
 
        # Create the FitnessDashboard table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS FitnessDashboard (
                FitnessDashboardID INTEGER PRIMARY KEY AUTOINCREMENT, 
                Date DATE, 
                MemberID INTEGER, 
                Steps INT, 
                Distance FLOAT, 
                CaloriesBurned INT, 
                Workouts INT, 
                TargetSteps INT, 
                TargetDistance FLOAT, 
                TargetCaloriesBurned INT, 
                TargetWorkouts INT, 
                BreakfastCalories INT, 
                LunchCalories INT, 
                DinnerCalories INT, 
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID) 
            ); 
        ''') 
 
             
        conn.commit() 
        conn.close() 
    except sqlite3.Error as e: 
        print(f"SQLite error: {e}") 
    finally: 
        if conn: 
            conn.close()
