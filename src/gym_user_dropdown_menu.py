class GymMainMenu: 
    def __init__(self, title,icon=None, function=None): 
        self.title = title 
        self.icon = icon 
        self.function = function  # Function to be called when the item is clicked 
        self.submenu = [] 
 
    def addSubMenu(self, subitem): 
        self.submenu.append(subitem) 
 
    def has_subitems(self): 
        return bool(self.submenu) 
 
def create_menu_section(): 
    def open_about_us(): 
        print("About Us clicked") 
 
    def open_mission(): 
        print("Mission clicked") 
 
    def open_staff_team(): 
        print("Staff & Team clicked") 
 
    def open_testimonials(): 
        print("Testimonials clicked") 
 
    def open_personal_trainer():
      print("Personal Trainer clicked") 
 
    def open_training_activities(): 
        print("Training Activities clicked") 
 
    def open_trainer_request(): 
        print("Trainer Request clicked") 
 
    def open_group_fitness_class(): 
        print("Group Fitness Class clicked") 
 
    def open_sports_training(): 
        print("Sports Training clicked") 
 
    def open_yoga_pilates(): 
        print("Yoga and Pilates clicked") 
 
    def open_nutrition_consultation(): 
        print("Nutrition Consultation clicked") 
 
    def open_membership_plan(): 
        print("Membership Plan clicked") 
 
    def open_membership_benefits(): 
        print("Membership Benefits clicked") 
 
    def open_how_to_join(): 
        print("How To Join clicked") 
 
    def open_schedule(): 
        print("Schedule clicked") 
 
    def open_class_description(): 
        print("Class Description clicked") 
 
    def open_booking_class(): 
        print("Booking Class clicked") 
 
    def open_gym_equipment(): 
        print("Gym Equipment clicked") 
 
    def open_cardio_machine(): 
        print("Cardio Machine clicked") 
 
    def open_pool(): 
        print("Pool clicked") 
 
    def open_sauna_steam_room():
        print("Sauna/Steam Room clicked") 
 
    def open_other_amenities(): 
        print("Other Amenities clicked") 
 
    def open_all_blogs(): 
        print("All Blogs clicked") 
 
    def open_home_workout(): 
        print("Home Workout clicked") 
 
    def open_fitness_tips(): 
        print("Fitness Tips clicked") 
 
    def open_nutrition_diet_tips(): 
        print("Nutrition & Diet Tips clicked") 
 
    def open_healthy_recipes(): 
        print("Healthy Recipes clicked") 
 
    def open_health_tips(): 
        print("Health Tips clicked") 
 
    def open_sports_improvement(): 
        print("Sports Improvement clicked") 
 
    def open_exercise_routines(): 
        print("Exercise Routines clicked") 
 
    def open_body_workout(): 
        print("Body Workout clicked") 
 
    def open_beginners_guide(): 
        print("Beginner's Guide clicked") 
 
    def open_elderly_guide(): 
        print("Elderly Guide clicked") 
 
    def open_women_workout(): 
        print("Women Workout clicked") 
 
    def open_gym_latest_updates(): 
        print("Gym Latest Updates clicked") 
 
    def open_faqs(): 
        print("FAQs clicked") 
 
    def open_membership_info(): 
        print("Membership Info clicked") 
 
    def open_contact_details(): 
        print("Contact Details clicked") 
 
    def open_social_media(): 
        print("Social Media clicked") 
 
    def open_reviews_ratings(): 
        print("Reviews & Ratings clicked") 
 
    def open_contact_form(): 
        print("Contact Form clicked") 
 
    def open_meals_page(): 
        print("Meal Page clicked") 
 
    def open_workouts_page(): 
        print("Workout Page clicked") 
 
    home = GymMainMenu("Home", icon="\u2302", function=None) 
    about_us = GymMainMenu("About Us", function=open_about_us) 
    mission = GymMainMenu("Mission", function=open_mission) 
    mission.addSubMenu(GymMainMenu("Staff & Team", function=open_staff_team)) 
    mission.addSubMenu(GymMainMenu("Testimonials", function=open_testimonials)) 
    about_us.addSubMenu(mission) 
    home.addSubMenu(about_us) 
 
    services = GymMainMenu("Services", icon="\u269B", function=None) 
    training_program = GymMainMenu("Training Program", function=None) 
    personal_training = GymMainMenu("Personal Training", function=None) 
    personal_training.addSubMenu(GymMainMenu("Personal Trainer", function=open_personal_trainer)) 
    personal_training.addSubMenu(GymMainMenu("Training Activities", function=open_training_activities)) 
    personal_training.addSubMenu(GymMainMenu("Trainer Request", function=open_trainer_request)) 
    training_program.addSubMenu(personal_training) 
    services.addSubMenu(training_program) 
    group_fitness_class = GymMainMenu("Group Fitness Class", function=open_group_fitness_class) 
    services.addSubMenu(group_fitness_class) 
    services.addSubMenu(GymMainMenu("Sports Training", function=open_sports_training)) 
    services.addSubMenu(GymMainMenu("Yoga and Pilates", function=open_yoga_pilates)) 
    services.addSubMenu(GymMainMenu("Nutrition Consultation", function=open_nutrition_consultation))
    home.addSubMenu(services) 
 
    membership = GymMainMenu("Membership", icon="\u2665", function=None) 
    membership.addSubMenu(GymMainMenu("Membership Plan", function=open_membership_plan)) 
    membership.addSubMenu(GymMainMenu("Membership Benefits", function=open_membership_benefits)) 
    membership.addSubMenu(GymMainMenu("How To Join", function=open_how_to_join)) 
    home.addSubMenu(membership) 
 
    fitness_classes = GymMainMenu("Fitness Classes", icon="\u266A", function=None) 
    fitness_classes.addSubMenu(GymMainMenu("Schedule", function=open_schedule)) 
    fitness_classes.addSubMenu(GymMainMenu("Class Description", function=open_class_description)) 
    fitness_classes.addSubMenu(GymMainMenu("Booking Class", function=open_booking_class)) 
    home.addSubMenu(fitness_classes) 
 
    fitness_amenities = GymMainMenu("Fitness Amenities", icon="\u2663", function=None) 
    fitness_amenities.addSubMenu(GymMainMenu("Gym Equipment", function=open_gym_equipment)) 
    fitness_amenities.addSubMenu(GymMainMenu("Cardio Machine", function=open_cardio_machine)) 
    fitness_amenities.addSubMenu(GymMainMenu("Pool", function=open_pool)) 
    fitness_amenities.addSubMenu(GymMainMenu("Sauna/Steam Room", function=open_sauna_steam_room)) 
    fitness_amenities.addSubMenu(GymMainMenu("Other Amenities", function=open_other_amenities)) 
    home.addSubMenu(fitness_amenities) 
 
    blogs_and_pages = GymMainMenu("Blogs & Pages", icon="\u270E", function=None) 
    all_blogs = GymMainMenu("All Blogs", icon="\u266A", function=None) 
    blogs_and_pages.addSubMenu(GymMainMenu("Meals Page", function=open_meals_page)) 
    blogs_and_pages.addSubMenu(GymMainMenu("Workouts Page", function=open_workouts_page)) 
    blogs_and_pages.addSubMenu(all_blogs) 
    home.addSubMenu(blogs_and_pages) 
     
    all_blogs.addSubMenu(GymMainMenu("Home Workout", function=open_home_workout)) 
    all_blogs.addSubMenu(GymMainMenu("Fitness Tips", function=None)) 
    all_blogs.addSubMenu(GymMainMenu("Sports Improvement", function=open_sports_improvement)) 
    all_blogs.addSubMenu(GymMainMenu("Exercise Routines", function=open_exercise_routines)) 
    all_blogs.addSubMenu(GymMainMenu("Body Workout", function=open_body_workout))
    all_blogs.addSubMenu(GymMainMenu("Beginner's Guide", function=open_beginners_guide)) 
    all_blogs.addSubMenu(GymMainMenu("Elderly Guide", function=open_elderly_guide)) 
    all_blogs.addSubMenu(GymMainMenu("Women Workout", function=open_women_workout)) 
    all_blogs.addSubMenu(GymMainMenu("Gym Latest Updates", function=open_gym_latest_updates)) 
 
    contact_us = GymMainMenu("Contact Us", icon="\u2706", function=None) 
    contact_us.addSubMenu(GymMainMenu("FAQs", function=open_faqs)) 
    contact_us.addSubMenu(GymMainMenu("Membership Info", function=open_membership_info)) 
    contact_us.addSubMenu(GymMainMenu("Contact Details", function=open_contact_details)) 
    contact_us.addSubMenu(GymMainMenu("Social Media", function=open_social_media)) 
    contact_us.addSubMenu(GymMainMenu("Reviews & Ratings", function=open_reviews_ratings)) 
    contact_us.addSubMenu(GymMainMenu("Contact Form", function=open_contact_form)) 
    home.addSubMenu(contact_us) 
 
    return home 
