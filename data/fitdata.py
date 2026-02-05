import sqlite3 
from sample_meal_data import * 
from sample_workout_data import * 
from sample_exercise_data import *  
 
def insert_sample_data(): 
    try: 
        conn = sqlite3.connect('FitZone.db') 
        cursor = conn.cursor() 
 
        # Sample data for GymLocations 
        gym_locations_data = [ 
            ('FitZone Central', '123 Main Street', 'info@fitzone.com', '123-456-7890'), 
            ('Downtown Fitness', '456 Elm Street', 'contact@downtownfit.com', 
'987-654-3210'), 
            ('Urban Gym', '789 Oak Avenue', 'info@urbangym.com', '555-555-5555') 
        ] 
 
        for data in gym_locations_data: 
            cursor.execute("INSERT INTO GymLocations (LocationName, Address, 
EmailAddress, ContactNumber) VALUES (?, ?, ?, ?)", data) 
 
        # Sample data for TeamLeaders 
        team_leaders_data = [ 
            ('Samuel Obigbesan', 'Manager', 'hero_section.jpg', 1) 
        ] 
 
        for data in team_leaders_data: 
            cursor.execute("INSERT INTO TeamLeaders (LeaderName, 
RoleDescription, ImagePath, LocationID) VALUES (?, ?, ?, ?)", data) 
 
        # Sample data for GymBenefits 
        gym_benefits_data = [ 
            ('Personalized workout plans', 1), 
            ('State-of-the-art fitness equipment', 1), 
            ('Experienced and certified trainers', 1), 
            ('Variety of group fitness classes', 1), 
            ('Relaxing sauna and spa facilities', 1), 
            ('Nutrition consultation services', 1), 
            ('Access to our online fitness resources', 1) 
        ] 
 
        for data in gym_benefits_data: 
            cursor.execute("INSERT INTO GymBenefits (BenefitName, LocationID) 
VALUES (?, ?)", data) 
 
        # Sample data for GymReviews 
        gym_reviews_data = [ 
            (1, 1, 'Really friendly and Helpful Staff', 'Great gym with friendly 
staff. There were lots of classes and equipments to use whilst at FitZone. I 
thoroughly enjoyed it.', 4, '2023-08-29'), 
            (1, 2, 'Limited Classes', 'Did not enjoy it. Classes were not fun.', 
1, '2023-08-21'), 
            (1, 4, 'Fair Gym', 'Decent Gym. I am now more productive.', 3, 
'2023-08-25') 
        ] 
 
        for data in gym_reviews_data: 
            cursor.execute("INSERT INTO GymReview (LocationID, ReviewerID, 
ReviewName, ReviewText, Rating, Date) VALUES (?, ?, ?, ?, ?, ?)", data) 

 
        # Sample data for GymReviews reply 
        gym_reviews_reply_data = [ 
            (1, 'Thank you for your feedback!', '2023-08-30'), 
            (2, 'We are sorry to hear that. We will improve our classes.', 
'2023-08-22') 
        ] 
 
        for data in gym_reviews_reply_data: 
            cursor.execute("INSERT INTO GymReply (ReviewID, ReplyText, 
ReplyDate) VALUES (?, ?, ?)", data) 
 
        # Insert sample data into GymAmenities table 
        cursor.execute(''' 
            INSERT INTO GymAmenities (LocationID, AmenityName) 
            VALUES 
                (1, 'Sauna'), (1, 'Group Classes'), (1, 'Locker Room'), 
                (2, 'Cardio Area'), (2, 'Yoga Studio'), (2, 'Steam Room'), 
                (3, 'Personal Training'), (3, 'Swimming Pool'); 
        ''') 
 
        # Insert sample data into GymEquipments table 
        cursor.execute(''' 
            INSERT INTO GymEquipments (LocationID, EquipmentName) 
            VALUES 
                (1, 'Treadmill'), (1, 'Dumbbells'), (1, 'Elliptical'), 
                (2, 'Rowing Machine'), (2, 'Bench Press'), (2, 'Cable Machine'), 
                (3, 'Squat Rack'), (3, 'Smith Machine'); 
        ''') 
 
        # Insert sample data into OpeningHours table 
        cursor.execute(''' 
            INSERT INTO OpeningHours (LocationID, Weekday, StartTime, EndTime) 
            VALUES 
                (1, 'Monday', '08:00:00', '21:00:00'), (1, 'Tuesday', 
'08:00:00', '21:00:00'), 
                (2, 'Monday', '07:00:00', '22:00:00'), (2, 'Tuesday', 
'07:00:00', '22:00:00'), 
                (3, 'Wednesday', '09:00:00', '20:00:00'), (3, 'Thursday', 
'09:00:00', '20:00:00'); 
        ''') 
         
        # Insert sample data into GymFeatures table 
        cursor.execute(''' 
            INSERT INTO GymFeatures (LocationID, FeatureName) 
            VALUES 
                (1, 'Personal Training'), (1, 'Swimming Pool'), 
                (2, 'Cycling Studio'), (2, 'Pilates Reformer'), 
                (3, 'Functional Training'), (3, 'CrossFit Area');
        ''') 
 
        # Insert sample data into Members table 
        cursor.execute(''' 
            INSERT INTO Members (LocationID, DurationID, PackageID, Username, 
Password, Salt, Gender, Email, DateOfBirth, JoinDate, FirstName, LastName, 
Address, CountryCode, PhoneNumber, ImagePath, EmailNotifications) 
            VALUES 
                (1, 2, 1, 'joseph_w', 'hashed_password', 'salt', 'Male', 
'john@example.com', '1990-01-15', '2023-01-01', 'Joseph', 'Well', '456 Elm 
Street', '+1', '987-654-3210', 'hero_section.jpg', 1), 
                (1, 2, 1, 'alexandra_p', 'hashed_password', 'salt', 'Female', 
'jane@example.com', '1988-05-20', '2023-02-15', 'Alexandra', 'Pit', '789 Maple 
Avenue', '+1', '123-456-7890', 'hero_section.jpg', 1), 
                (1, 2, 2, 'Samuel123', 'hashed_password', 'salt', 'Male', 
'SObigbesan17@gmail.com', '1995-03-12', '2023-03-01', 'Samuel', 'O', '123 Oak 
Lane', '+1', '555-555-5555', 'hero_section.jpg', 1), 
                (1, 1, 1, 'alfie_b', 'hashed_password', 'salt', 'Male', 
'alfie@example.com', '1998-08-05', '2023-04-15', 'Alfie', 'B', '789 Elm Street', 
'+1', '999-999-9999', 'hero_section.jpg', 1), 
                (1, 2, 1, 'lucy_w', 'hashed_password', 'salt', 'Female', 
'lucy@example.com', '1992-11-25', '2023-05-10', 'Lucy', 'Wilson', '234 Pine 
Road', '+1', '777-777-7777', 'hero_section.jpg', 1); 
        ''') 
 
        # Insert sample data into the Testimonials table 
        cursor.execute(''' 
            INSERT INTO Testimonials (MemberID, TestimonialText, 
TestimonialDate, ImagePath, FrameColor, NameColor, TestimonialColor) 
            VALUES 
                (1, 'This is a great product!', '2023-08-15', 
'hero_section.jpg', '#FF5733', '#A3D7E0', '#7D3C98'), 
                (2, 'I love the quality of their services.', '2023-08-16', 
'hero_section.jpg', '#FFC300', '#FF5733', '#C70039'), 
                (3, 'Highly recommend their class.', '2023-08-17', 
'hero_section.jpg', '#900C3F', '#FF5733', '#00A859'), 
                (4, 'Lots of activities and events to be a part of!', '2023-08
18', 'hero_section.jpg', '#FF5733', '#FFC300', '#900C3F'), 
                (5, 'Amazing experience with this company.', '2023-08-19', 
'hero_section.jpg', '#7D3C98', '#00A859', '#FFC300'); 
        ''') 
 
        # Insert sample data for MembershipPackages 
        membership_packages_data = [ 
            (1, 'Basic Package', 'Access to gym facilities'), 
            (1, 'Premium Package', 'Access to gym facilities + classes') 
        ] 
 
        for data in membership_packages_data: 
            cursor.execute("INSERT INTO MembershipPackages (LocationID, 
PackageName, Description) VALUES (?, ?, ?)", data) 
 
        # Insert sample data for MembershipDurations 
        membership_durations_data = [ 
            ('Monthly', '1 months membership', 30, 1), 
            ('Quarterly', '3 month membership', 120, 1), 
            ('Yearly', '12 months membership', 365, 1) 
        ] 
 
        for data in membership_durations_data: 
            cursor.execute("INSERT INTO MembershipDurations (DurationName, 
Description, NumberOfDays, LocationID) VALUES (?, ?, ?, ?)", data) 
 
        # Insert sample data for MembershipPrices 
        membership_prices_data = [ 
            (1, 1, 50.00), 
            (1, 2, 150.00), 
            (2, 1, 90.00), 
            (2, 2, 190.00), 
            (3, 1, 130.00), 
            (3, 2, 230.00) 
        ] 
 
        for data in membership_prices_data: 
            cursor.execute("INSERT INTO MembershipPrices (DurationID, PackageID, 
Price) VALUES (?, ?, ?)", data) 
 
        # Insert sample data for MembershipPackagesFeatures 
        membership_features_data = [ 
            (1, 'Personal Training', 1), 
            (1, 'Swimming Pool', 0), 
            (1, 'Cycling Studio', 1), 
            (1, 'Pilates Reformer', 0), 
            (2, 'Personal Training', 1), 
            (2, 'Swimming Pool', 1), 
            (2, 'Cycling Studio', 1), 
            (2, 'Pilates Reformer', 1) 
        ] 
 
        for data in membership_features_data: 
            cursor.execute("INSERT INTO MembershipPackagesFeatures (PackageID, 
FeatureName, IsIncluded) VALUES (?, ?, ?)", data) 
 
        # Insert sample data for DailyPrices 
        daily_prices_data = [ 
            (1, 5.99, 1), (2, 5.99, 1), 
            (7, 5.99, 1), (30, 5.99, 1),
                        (1, 7.99, 2), (2, 7.99, 2), 
            (7, 7.99, 2), (30, 7.99, 2), 
            (1, 5.99, 3), (7, 5.99, 3) 
        ] 
 
        for data in daily_prices_data: 
            cursor.execute("INSERT INTO DailyPrices (NumberOfDays, Price, 
LocationID) VALUES (?, ?, ?)", data) 
 
        # Insert sample data for GymClasses 
        gym_classes_data = [ 
            ('Zumba', 20, 1, 1), 
            ('Yoga', 15, 2, 2), 
            ('Spin', 10, 3, 1) 
        ] 
 
        for data in gym_classes_data: 
            cursor.execute("INSERT INTO GymClasses (ClassName, AvailableSlots, 
InstructorID, StudioID) VALUES (?, ?, ?, ?)", data) 
 
        # Insert sample data for Instructors 
        instructors_data = [ 
            ('Alexa', 1, 'hero_section.jpg'), 
            ('John', 1, 'hero_section.jpg'), 
            ('Sarah', 1, 'hero_section.jpg') 
        ] 
 
        for data in instructors_data: 
            cursor.execute("INSERT INTO Instructors (InstructorName, LocationID, 
ImagePath) VALUES (?, ?, ?)", data) 
 
        # Insert sample data for Staff 
        staff_data = [ 
            ('John Smith', 'Trainer', 1, 'Male', 'john@example.com', '1985-03
20', '2023-01-15', 'John', 'Smith', '123 Oak Street', '555-123-4567', 
'hero_section.jpg'), 
            ('Alice Johnson', 'Front Desk', 2, 'Female', 'alice@example.com', 
'1990-06-10', '2023-02-20', 'Alice', 'Johnson', '456 Maple Avenue', '987-654
3210', 'hero_section.jpg'), 
            ('Robert Brown', 'Manager', 1, 'Male', 'robert@example.com', '1978
11-30', '2023-03-05', 'Robert', 'Brown', '789 Elm Lane', '123-456-7890', 
'hero_section.jpg'), 
            ('Emma Davis', 'Instructor', 3, 'Female', 'emma@example.com', '1993
04-15', '2023-04-10', 'Emma', 'Davis', '234 Pine Road', '555-555-5555', 
'hero_section.jpg'), 
            ('William Taylor', 'Trainer', 2, 'Male', 'william@example.com', 
'1987-09-25', '2023-05-01', 'William', 'Taylor', '345 Cedar Avenue', '999-999
9999', 'hero_section.jpg') 
        ] 

 
        for data in staff_data: 
            cursor.execute("INSERT INTO Staff (StaffName, RoleDescription, 
LocationID, Gender, Email, DateOfBirth, JoinDate, FirstName, LastName, Address, 
PhoneNumber, ImagePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data) 
 
        class_schedule_data = [ 
            (1, '10:00', '2023-10-29', '01:00', ''), 
            (1, '14:30', '2023-10-30', '00:45', ''), 
            (2, '16:30', '2023-10-29', '00:45', ''), 
            (3, '14:40', '2023-10-30', '00:45', ''), 
            (2, '09:00', '2023-11-01', '01:30', ''), 
            (3, '11:15', '2023-10-30', '01:15', ''), 
            (1, '13:55', '2023-10-31', '00:30', ''), 
            (2, '14:00', '2023-11-01', '00:45', ''), 
            (3, '10:30', '2023-11-02', '01:00', ''), 
            (1, '17:15', '2023-11-01', '00:45', ''), 
            (2, '11:30', '2023-11-03', '01:15', ''), 
            (2, '13:30', '2023-11-01', '01:15', ''), 
            (1, '10:30', '2023-11-03', '00:45', ''), 
            (3, '03:30', '2023-10-30', '03:55', ''), 
            (1, '10:00', '2023-10-29', '01:00', ''), 
            (1, '14:30', '2023-10-30', '00:45', ''), 
            (2, '16:30', '2023-10-29', '00:45', ''), 
            (3, '14:40', '2023-10-30', '00:45', ''), 
            (3, '14:45', '2023-10-30', '00:45', ''), 
            (3, '16:00', '2023-10-29', '00:45', ''), 
        ] 
         
        for data in class_schedule_data: 
            cursor.execute("INSERT INTO ClassSchedule (ClassID, StartTime, Date, 
Duration, Message) VALUES (?, ?, ?, ?, ?)", data) 
 
        enrollment_data = [ 
            (1, 1),  
            (1, 2), 
            (1, 3), 
        ] 
 
        for data in enrollment_data: 
            cursor.execute('INSERT INTO Enrollment (MemberID, ClassID) VALUES 
(?, ?)', data) 
 
        sample_data = [ 
            (1, '2023-01-01', 70.5, 175.0, 20.0, 55.0, 350, 75, '120/80', 7.5, 
10000, 2000, 2500, 'Cardio', 45, 'Moderate', 'Happy'), 
            (1, '2023-01-15', 70.0, 175.0, 19.5, 55.5, 375, 77, '122/82', 7.0, 
11000, 2100, 2600, 'Cardio', 50, 'Moderate', 'Happy'), 
            (1, '2023-01-30', 69.5, 175.5, 19.0, 56.0, 400, 80, '125/85', 7.2, 12000, 2200, 2700, 'Cardio', 55, 'Moderate', 'Happy'), 
        ] 
 
        # Insert sample data into the GymStudios table 
        cursor.execute(''' 
            INSERT INTO GymStudios (StudioName, Capacity, LocationID) 
            VALUES 
            ('Studio A', 30, 1), 
            ('Studio B', 20, 1), 
            ('Studio C', 25, 2); 
        ''') 
 
        # Insert data into FAQs table 
        faqs_data = [ 
            (1, 'How do I sign up for a membership?', 'You can sign up for a 
membership by visiting our gym\'s front desk. Our friendly staff will assist you 
in selecting the right membership package for your needs.'), 
            (1, 'What are the membership pricing options?', 'We offer a variety 
of membership packages with different pricing options. You can find detailed 
pricing information at our front desk or on our website.'), 
            (1, 'Are personal trainers available?', 'Yes, we have experienced 
personal trainers who can help you create a customized fitness plan to achieve 
your goals. You can schedule sessions with them at the gym.'), 
            (1, 'What are the gym operating hours?', 'Our gym is open seven days 
a week. Our hours of operation are as follows: Monday to Friday: 5:00 AM - 10:00 
PM, Saturday and Sunday: 7:00 AM - 8:00 PM.'), 
            (1, 'Are group fitness classes available?', 'Yes, we offer a variety 
of group fitness classes suitable for all fitness levels. Check our class 
schedule for details on class times and types.'), 
            (1, 'Do you have locker facilities?', 'Yes, we provide locker 
facilities for our members to store their belongings  while they work out.'), 
            (1, 'How can I contact the gym for further inquiries?', 'You can 
reach us at the following contact information: Email: example@email.com, Phone: 
+1234567890') 
        ] 
 
        for data in faqs_data: 
            cursor.execute("INSERT INTO FAQs (LocationID, Question, Answer) 
VALUES (?, ?, ?)", data) 
 
        # Insert data into Meal Schedule table 
        meal_schedule_data = [ 
            ('2023-09-02', 'Breakfast', 1, 1, 1), 
            ('2023-09-02', 'Lunch', 2, 1, 2), 
            ('2023-09-02', 'Dinner', 3, 4, 3), 
            ('2023-09-03', 'Breakfast', 1, 1, 4), 
            ('2023-09-03', 'Lunch', 2, 3, 5), 
            ('2023-09-03', 'Dinner', 3, 4, 1) 
        ]
 
        for data in meal_schedule_data: 
            cursor.execute("INSERT INTO MealSchedule (Date, Time, MealID, 
CustomMealID, MemberID) VALUES (?, ?, ?, ?, ?)", data) 
 
 
        data = [ 
            ("(CUSTOM) Bread and egg", "Breakfast", "A classic breakfast 
option", 300, 10.0, 15.0, 30.0, "Bread, egg, butter", "00:15:00", 
"breadandegg.jpg", "breadandegg.txt", "Weight Loss", 5.0, "None", "None", 200, 
1), 
            ("(CUSTOM) Beans on toast", "Breakfast", "A hearty breakfast with 
beans on toast", 350, 12.5, 10.0, 45.0, "Bread, baked beans, butter", 
"00:20:00", "beansontoast.jpg", "cereal.txt", "Maintenance", 7.0, "None", 
"None", 300, 1), 
            ("(CUSTOM) Cereals", "Breakfast", "A quick and easy breakfast 
choice", 250, 5.0, 2.5, 60.0, "Cereal, milk, sugar", "00:05:00", "cereal.jpg", 
"cereal.txt", "Weight Gain", 6.0, "Vegetarian", "None", 150, 2) 
        ] 
 
        # Insert data into CustomMeals table using a loop 
        for meal_data in data: 
            cursor.execute('''INSERT INTO CustomMeals (MealName, MealType, 
Summary, Calories, Protein, Fat, Carbohydrates, Ingredients, CookingTime, 
ImagePath, FilePath, NutritionalGoals, Budget, DietaryRestrictions, Allergies, 
MealSize, MemberID) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
?, ?)''', meal_data) 
             
        # Insert sample data into Meals table 
        with open('meals_data.csv', 'r') as csv_file: 
            csv_reader = csv.reader(csv_file) 
             
            next(csv_reader, None) 
             
            # Inserting csv data into the Meals table 
            for row in csv_reader: 
                meal = (row[0], row[1], row[2], int(row[3]), float(row[4]), 
float(row[5]), float(row[6]), row[7], int(row[8]), row[9], row[10], row[11], 
float(row[12]), row[13], row[14], row[15]) 
                 
                cursor.execute(''' 
                    INSERT INTO Meals ( 
                        MealName, MealType, Summary, Calories, Protein, Fat, 
Carbohydrates, 
                        Ingredients, CookingTime, ImagePath, FilePath, 
NutritionalGoals, Budget, DietaryRestrictions, Allergies, MealSize 
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', meal) 
 
        # Sample data to insert into MealReviews 
        meal_review_data = [ 
            (1, 4, "Delicious meal!", 5), 
            (2, 2, "Good but could be better", 3), 
            (3, 1, "Amazing taste!", 5), 
            (4, 3, "Healthy and satisfying", 4), 
            (5, 4, "Not my favorite", 2), 
        ] 
 
        # Insert sample data into MealReviews 
        for data in meal_review_data: 
            cursor.execute("INSERT INTO MealReviews (ReviewID, MealID, Comment, 
Rating) VALUES (?, ?, ?, ?)", data) 
 
        # Insert sample data into Workouts 
        with open('workouts_data.csv', 'r') as csv_file: 
            csv_reader = csv.reader(csv_file) 
            next(csv_reader, None)   
            for row in csv_reader: 
                workout = ( 
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                    int(row[7]), int(row[8])   
                ) 
                cursor.execute(''' 
                    INSERT INTO Workouts ( 
                        WorkoutName, WorkoutType, WorkoutGoal, Description, 
Difficulty, ImagePath, 
                        Equipment, WarmupDuration, CooldownDuration 
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', workout) 
 
        # Insert sample data into Exercises 
        with open('exercises_data.csv', 'r') as csv_file: 
            csv_reader = csv.reader(csv_file) 
             
            next(csv_reader, None)  
             
            for row in csv_reader: 
                exercise = (row[0], row[1], row[2], row[3], row[4], int(row[5]), 
row[6]) 
                 
                cursor.execute(''' 
                    INSERT INTO Exercises ( 
                        ExerciseName, ExerciseType, Description, Difficulty, 
TargetedBodyPart, Duration, ImagePath 
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', exercise) 
                 
        # Insert sample data into WorkoutExercises 
        cursor.execute(''' 
            INSERT INTO WorkoutExercises (WorkoutID, ExerciseID) 
            VALUES 
            (1, 1), 
            (1, 2), 
            (1, 4), 
            (2, 3), 
            (2, 5), 
            (2, 6), 
            (3, 2), 
            (3, 4), 
            (3, 7), 
            (4, 1), 
            (4, 3), 
            (4, 5), 
            (5, 6), 
            (5, 8), 
            (5, 9), 
            (6, 1), 
            (6, 10), 
            (6, 11), 
            (7, 5), 
            (7, 9), 
            (7, 12), 
            (8, 2), 
            (8, 6), 
            (8, 10), 
            (9, 4), 
            (9, 8), 
            (9, 12), 
            (10, 1), 
            (10, 3), 
            (10, 5), 
            (11, 7), 
            (11, 9), 
            (11, 11), 
            (12, 2), 
            (12, 4), 
            (12, 6), 
            (13, 8), 
            (13, 10), 
            (13, 12) 
        ''') 
 
        # Insert sample data into WorkoutReviews 
        cursor.execute(''' 
            INSERT INTO WorkoutReviews (MemberID, WorkoutID, Rating, Title, 
Comment) 
            VALUES 
            (1, 1, 5, 'Great workout!', 'I loved the morning routine.'), 
            (2, 2, 4, 'Nice run', 'Enjoyed the evening run.') 
        ''') 
 
        # Insert sample data into WorkoutSchedules 
        cursor.execute(''' 
            INSERT INTO WorkoutSchedules (MemberID, WorkoutID, ScheduledDate, 
ScheduledTime) 
            VALUES 
            (1, 1, '2023-09-10', '08:00'), 
            (2, 2, '2023-09-12', '18:00') 
        ''') 
 
        # Fitness Dashboard 
        fitness_data = [ 
            (datetime.date.today(), 1, 7500, 5.2, 450, 6, 10000, 8.0, 600, 3, 
300, 400, 600), 
            (datetime.date.today() - datetime.timedelta(days=1), 6, 8000, 5.5, 
480, 2, 10000, 8.0, 600, 3, 350, 420, 610), 
            (datetime.date.today() - datetime.timedelta(days=2), 6, 7200, 4.8, 
430, 1, 10000, 8.0, 600, 3, 320, 390, 590), 
            (datetime.date.today() - datetime.timedelta(days=3), 6, 7600, 5.0, 
460, 0, 10000, 8.0, 600, 3, 310, 410, 580), 
            (datetime.date.today() - datetime.timedelta(days=4), 6, 7800, 5.3, 
490, 1, 10000, 8.0, 600, 3, 330, 420, 600), 
            (datetime.date.today() - datetime.timedelta(days=5), 6, 7100, 4.7, 
420, 2, 10000, 8.0, 600, 3, 280, 380, 570), 
            (datetime.date.today() - datetime.timedelta(days=6), 6, 7300, 4.9, 
440, 1, 10000, 8.0, 600, 3, 310, 400, 590), 
            (datetime.date.today() - datetime.timedelta(days=7), 6, 7600, 5.1, 
470, 0, 10000, 8.0, 600, 3, 320, 410, 610), 
        ] 
 
        # Insert the sample data into the FitnessDashboard table 
        cursor.executemany(''' 
            INSERT INTO FitnessDashboard (Date, MemberID, Steps, Distance, 
CaloriesBurned, Workouts, TargetSteps, TargetDistance, TargetCaloriesBurned, 
TargetWorkouts, BreakfastCalories, LunchCalories, DinnerCalories) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        ''', fitness_data) 
 
        conn.commit() 
        print("Sample data inserted successfully.") 
 
    except sqlite3.Error as e: 
        print(f"SQLite error: {e}") 

    finally: 
        if conn: 
            conn.close()
