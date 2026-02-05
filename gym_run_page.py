import tkinter as tk 
from gym_home_page import * 
from gym_login import * 
from gym_header import * 
from gym_forgot_password import * 
from gym_account_verification import * 
from gym_set_new_password import * 
from gym_select_your_gym_page import * 
from gym_membership_duration_registration_page import * 
from gym_membership_package_registration_page import * 
from gym_user_details_registration_page import * 
from gym_payment_registration_page import * 
from gym_registration_success_page import * 
from gym_meal_page import * 
from gym_workouts_page import * 
from gym_fitness_dashboard_page import * 
from gym_personalised_meal_planner import * 
from gym_personalised_workout_planner import * 
from gym_features_registration_page import * 
from gym_view_the_gym_team import * 
from gym_booking_class_page import * 
from gym_reviews_page import * 
from gym_calculate_bmi_page import * 
from gym_bmi_visualisation_report_page import * 
from gym_view_member_class_schedule_page import * 
from gym_view_member_class_clashes_page import * 
from gym_class_reservations_page import * 
from gym_modify_classes_page import * 
from gym_user_update_profile_page import * 
 
class GymManager:
    def __init__(self): 
        self.login_window = None 
        self.home_page_window = None  
        self.forgot_password_window = None 
        self.account_verification_window = None 
        self.set_new_password_window = None 
        self.select_your_gym_window = None 
        self.membership_duration_window = None 
        self.membership_package_window = None 
        self.user_detail_registration_window = None 
        self.payment_registration_window = None 
        self.registration_success_window = None 
        self.meal_page_window = None 
        self.workout_page_window = None 
        self.fitness_dashboard_page_window = None 
        self.personalised_meal_planner_window = None 
        self.personalised_workout_planner_window = None 
        self.gym_features_window = None 
        self.gym_view_team_window = None 
        self.gym_classes_booking_window = None 
        self.gym_reviews_window = None 
        self.calculate_bmi_window = None 
        self.run_bmi_visualisation_window = None 
        self.view_member_class_schedule_window = None 
        self.view_member_class_clashes_window = None 
        self.class_reserve_slot_window = None 
        self.leave_class_window = None 
        self.update_profile_window = None 
        self.member_id = None 
        self.location_id = None 
        self.class_id = None 
        self.class_schedule_id = None 
        self.message_error = None 
 
    def create_header(self, page): 
        try: 
            header = GymHeader(page, self.run_login_page, self.run_logout, 
self.run_update_profile_page, self.run_home_page, 
                               self.run_meals_page, self.run_workouts_page, 
self.member_id) 
            header.place(relx=0, rely=0, relwidth=1) 
 
        except Exception as e: 
            print("Error creating Header:", e) 
 
    def create_progress_bar(self, page, progress_value): 
        try: 
            self.progress_bar = HorizontalProgressBar(page, progress_value) 
            self.progress_bar.frame.place(relx=0, rely=0.06, relwidth=1)
 
        except Exception as e: 
            print("Error creating Progress Bar:", e) 
 
 
    def run_home_page(self): 
        if self.member_id: 
            self.run_fitness_dashboard_page() 
        else: 
            self.destroy_all_pages() 
            self.home_page_window = GymHomePage(self.run_select_your_gym_page, 
self.run_gym_features_page) 
            self.create_header(self.home_page_window) 
            self.home_page_window.update() 
            self.maximize_window(self.home_page_window) 
 
    def run_login_page(self): 
        self.destroy_all_pages() 
        self.login_window = GymLogin(self.run_select_your_gym_page, 
self.run_forgot_password_page, self.run_successful_login, self.message_error) 
        self.create_header(self.login_window) 
        self.login_window.update() 
        self.maximize_window(self.login_window) 
 
    def run_logout(self): 
        self.destroy_all_pages() 
        self.member_id = None 
        self.run_home_page() 
 
    def run_successful_login(self): 
        self.member_id = self.login_window.get_member_id() # Retrieve MemberID 
        self.location_id = self.login_window.get_location_id() # Retrieve 
LocationID 
        time.sleep(3) 
        self.destroy_all_pages() 
        self.run_home_page() 
 
    def run_forgot_password_page(self): 
        self.destroy_all_pages() 
        self.forgot_password_window = 
GymForgotPassword(self.run_account_verification_page) 
        self.create_header(self.forgot_password_window) 
        self.forgot_password_window.update() 
        self.maximize_window(self.forgot_password_window) 
 
    def run_account_verification_page(self): 
        email = self.forgot_password_window.get_email() # Retrieve Email 
        username = self.forgot_password_window.get_username() # Retrieve Username 
        self.destroy_all_pages() 
         
        self.account_verification_window = GymAccountVerification(email, 
username, self.run_set_new_password_page)  
        self.create_header(self.account_verification_window) 
        self.account_verification_window.update() 
        self.maximize_window(self.account_verification_window) 
 
    def run_set_new_password_page(self): 
        member_id = self.account_verification_window.get_member_id() # Retrieve 
Member ID 
        self.destroy_all_pages() 
         
        self.set_new_password_window = GymSetNewPassword(member_id, 
self.run_login_page)  
        self.create_header(self.set_new_password_window) 
        self.set_new_password_window.update() 
        self.maximize_window(self.set_new_password_window) 
 
    def run_select_your_gym_page(self): 
        self.destroy_all_pages() 
        self.select_your_gym_window = 
GymSelectionPage(self.run_membership_duration_page) 
        self.create_header(self.select_your_gym_window) 
        self.create_progress_bar(self.select_your_gym_window, 0) 
        self.select_your_gym_window.update() 
        self.maximize_window(self.select_your_gym_window) 
 
    def run_membership_duration_page(self): 
        self.location_id = self.select_your_gym_window.get_location_id() # 
Retrieve Location ID 
        self.destroy_all_pages() 
        self.membership_duration_window = 
GymMembershipDurationPage(self.location_id, self.run_membership_package_page) 
        self.create_header(self.membership_duration_window) 
        self.create_progress_bar(self.membership_duration_window, 20) 
        self.membership_duration_window.update() 
        self.maximize_window(self.membership_duration_window) 
 
    def run_membership_package_page(self): 
        self.membership_duration_id = 
self.membership_duration_window.get_membership_duration_id() # Retrieve Number 
of Days ID 
        self.number_of_days_id = 
self.membership_duration_window.get_membership_number_of_days_id() # Retrieve 
Duration ID 
        self.membership_price = 
self.membership_duration_window.get_membership_price() 
 
        self.destroy_all_pages() 
 
        if self.membership_duration_id != 0: 
            self.membership_package_window = 
GymMembershipPackagePage(self.location_id, self.membership_duration_id, 
self.run_user_detail_registration_page) 
            self.create_progress_bar(self.select_your_gym_window, 40) 
            self.create_header(self.membership_package_window) 
            self.membership_package_window.update() 
            self.maximize_window(self.membership_package_window) 
        else: 
            self.run_user_detail_registration_page() 
 
    def run_user_detail_registration_page(self): 
        self.member_package_id = 0 
        if self.membership_duration_id != 0: 
            self.member_package_id = 
self.membership_package_window.get_membership_package_id() 
            self.membership_price = 
self.membership_package_window.get_membership_price() 
             
        self.destroy_all_pages() 
  
        self.user_detail_registration_window = 
GymDetailsRegistrationPage(self.run_payment_registration_page) 
        self.create_header(self.user_detail_registration_window) 
        self.create_progress_bar(self.user_detail_registration_window, 60) 
        self.user_detail_registration_window.update() 
        self.maximize_window(self.user_detail_registration_window) 
 
    def run_payment_registration_page(self): 
        self.users_detail = 
self.user_detail_registration_window.get_user_account_details() 
         
        self.destroy_all_pages() 
 
        self.payment_registration_window = GymPaymentPage(self.membership_price, 
self.run_registration_success_page) 
        self.create_header(self.payment_registration_window) 
        self.create_progress_bar(self.payment_registration_window, 80) 
        self.payment_registration_window.update() 
        self.maximize_window(self.payment_registration_window) 
 
    def run_registration_success_page(self): 
        self.destroy_all_pages() 
        self.member_detail = [self.location_id, self.membership_duration_id, 
self.member_package_id] + self.users_detail
        self.registration_success_window = 
GymRegistrationSuccessPage(self.member_detail, self.run_home_page) 
        self.create_header(self.registration_success_window) 
        self.create_progress_bar(self.registration_success_window, 100) 
        self.registration_success_window.update() 
        self.maximize_window(self.registration_success_window) 
 
    def run_meals_page(self): 
        self.destroy_all_pages() 
        self.meal_page_window = MealsPostPage()  
        self.create_header(self.meal_page_window) 
        self.meal_page_window.update() 
        self.maximize_window(self.meal_page_window) 
 
    def run_workouts_page(self): 
        self.destroy_all_pages() 
        self.workout_page_window = WorkoutsPage()  
        self.create_header(self.workout_page_window) 
        self.workout_page_window.update() 
        self.maximize_window(self.workout_page_window) 
 
    def run_fitness_dashboard_page(self): 
        self.destroy_all_pages() 
        self.fitness_dashboard_page_window = 
FitnessDashboardPage(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.fitness_dashboard_page_window) 
        self.fitness_dashboard_page_window.update() 
        self.maximize_window(self.fitness_dashboard_page_window) 
 
    def run_personalised_meal_planner_page(self): 
        self.destroy_all_pages() 
        self.personalised_meal_planner_window = 
GymPersonalisedMealPlanner(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.personalised_meal_planner_window) 
        self.personalised_meal_planner_window.update() 
        self.maximize_window(self.personalised_meal_planner_window) 
    def run_personalised_workout_planner_page(self): 
        self.destroy_all_pages() 
        self.personalised_workout_planner_window = 
GymPersonalisedWorkoutPlanner(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.personalised_workout_planner_window) 
        self.personalised_workout_planner_window.update() 
        self.maximize_window(self.personalised_workout_planner_window) 
 
    def run_gym_features_page(self): 
        if self.home_page_window: 
            self.location_id = self.home_page_window.get_location_id() # 
Retrieve Location ID 
        try: 
            self.destroy_all_pages() 
            self.gym_features_window = GymFeaturesPage(self.location_id, 
self.run_gym_features_page, self.run_gym_view_team_page, 
self.run_gym_classes_booking_page, self.run_gym_reviews_page) 
            self.create_header(self.gym_features_window) 
            self.gym_features_window.update() 
            self.maximize_window(self.gym_features_window) 
        except: 
            self.destroy_all_pages() 
            self.run_home_page() 
 
    def run_gym_view_team_page(self): 
        self.destroy_all_pages() 
        self.gym_view_team_window = GymViewTeamPage(self.location_id, 
self.run_gym_features_page, self.run_gym_view_team_page, 
self.run_gym_classes_booking_page, self.run_gym_reviews_page) 
        self.create_header(self.gym_view_team_window) 
        self.gym_view_team_window.update() 
        self.maximize_window(self.gym_view_team_window) 
 
    def run_gym_classes_booking_page(self): 
        self.destroy_all_pages() 
        self.gym_classes_booking_window = GymClassBookingPage(self.location_id, 
self.member_id, self.run_gym_features_page, self.run_gym_view_team_page, 
self.run_gym_classes_booking_page, 
                                                              
self.run_gym_reviews_page, self.run_class_reservation_page) 
        self.create_header(self.gym_classes_booking_window) 
        self.gym_classes_booking_window.update() 
        self.maximize_window(self.gym_classes_booking_window)
 
    def run_gym_reviews_page(self): 
        self.destroy_all_pages() 
        self.gym_reviews_window = GymReviewPage(self.location_id, 
self.run_gym_features_page, self.run_gym_view_team_page, 
self.run_gym_classes_booking_page, self.run_gym_reviews_page) 
        self.create_header(self.gym_reviews_window) 
        self.gym_reviews_window.update() 
        self.maximize_window(self.gym_reviews_window) 
 
    def run_calculate_bmi_page(self): 
        self.destroy_all_pages() 
        self.calculate_bmi_window = CalculateBMIPage(self.member_id, 
self.run_fitness_dashboard_page, self.run_calculate_bmi_page, 
self.run_bmi_visualisation_report_page, self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.calculate_bmi_window) 
        self.calculate_bmi_window.update() 
        self.maximize_window(self.calculate_bmi_window) 
 
    def run_bmi_visualisation_report_page(self): 
        self.destroy_all_pages() 
        self.run_bmi_visualisation_window = 
BMIVisualisationReportPage(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.run_bmi_visualisation_window) 
        self.run_bmi_visualisation_window.update() 
        self.maximize_window(self.run_bmi_visualisation_window) 
 
    def run_view_member_class_schedule_page(self): 
        self.destroy_all_pages() 
        self.view_member_class_schedule_window = 
MemberClassSchedulePage(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page, self.run_modify_classes_page) 
        self.create_header(self.view_member_class_schedule_window) 
        self.view_member_class_schedule_window.update()
        self.maximize_window(self.view_member_class_schedule_window) 
 
    def run_view_member_class_clashes_page(self): 
        self.destroy_all_pages() 
        self.view_member_class_clashes_window = 
MemberClassClashesPage(self.member_id, self.run_fitness_dashboard_page, 
self.run_calculate_bmi_page, self.run_bmi_visualisation_report_page, 
self.run_personalised_meal_planner_page, 
                                                                            
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_modify_classes_page, 
                                                                       
self.run_view_member_class_clashes_page) 
        self.create_header(self.view_member_class_clashes_window) 
        self.view_member_class_clashes_window.update() 
        self.maximize_window(self.view_member_class_clashes_window) 
 
    def run_class_reservation_page(self): 
        if self.member_id: # If user is already logged in 
            self.class_id = self.gym_classes_booking_window.get_class_id() # 
Retrieve Class ID 
            self.destroy_all_pages() 
            self.view_member_class_schedule_window = 
GymClassReservationPage(self.class_id, self.member_id, 
self.run_gym_features_page, self.run_gym_view_team_page, 
self.run_gym_classes_booking_page, 
                                                                  
self.run_gym_reviews_page) 
            self.create_header(self.view_member_class_schedule_window) 
            self.view_member_class_schedule_window.update() 
            self.maximize_window(self.view_member_class_schedule_window) 
        else: 
            self.message_error = "Error: \n\n \u26A0 Please log in to book 
classes." 
            self.run_login_page() 
 
    def run_modify_classes_page(self): 
        if self.view_member_class_schedule_window: 
            self.class_schedule_id = 
self.view_member_class_schedule_window.get_class_schedule_id() # Retrieve Class 
ID 
        self.destroy_all_pages() 
        self.leave_class_window = LeaveClassPage(self.class_schedule_id, 
self.member_id, self.run_fitness_dashboard_page, self.run_calculate_bmi_page, 
self.run_bmi_visualisation_report_page, self.run_personalised_meal_planner_page, 
                                                                              
self.run_personalised_workout_planner_page, 
self.run_view_member_class_schedule_page, self.run_gym_classes_booking_page, 
self.run_view_member_class_clashes_page) 
        self.create_header(self.leave_class_window) 
        self.leave_class_window.update() 
        self.maximize_window(self.leave_class_window) 
 
    def run_update_profile_page(self): 
        self.destroy_all_pages() 
        self.update_profile_window = GymUpdateProfile(self.member_id) 
        self.create_header(self.update_profile_window) 
        self.update_profile_window.update() 
        self.maximize_window(self.update_profile_window) 
                 
    def destroy_all_pages(self): 
        if self.login_window is not None: 
            self.login_window.destroy() 
            self.login_window = None 
 
        if self.home_page_window is not None: 
            self.home_page_window.destroy() 
            self.home_page_window = None 
 
        if self.forgot_password_window is not None: 
            self.forgot_password_window.destroy() 
            self.forgot_password_window = None 
 
        if self.account_verification_window is not None: 
            self.account_verification_window.destroy() 
            self.account_verification_window = None 
 
        if self.set_new_password_window is not None: 
            self.set_new_password_window.destroy() 
            self.set_new_password_window = None 
 
        if self.select_your_gym_window is not None: 
            self.select_your_gym_window.destroy() 
            self.select_your_gym_window = None 
 
        if self.select_your_gym_window is not None: 
            self.select_your_gym_window.destroy() 
            self.select_your_gym_window = None 
 
        if self.membership_duration_window is not None: 
            self.membership_duration_window.destroy() 
            self.membership_duration_window = None 
 
        if self.membership_package_window is not None: 
            self.membership_package_window.destroy() 
            self.membership_package_window = None 
 
        if self.user_detail_registration_window is not None: 
            self.user_detail_registration_window.destroy() 
            self.user_detail_registration_window = None 
 
        if self.payment_registration_window is not None: 
            self.payment_registration_window.destroy() 
            self.payment_registration_window = None 
 
        if self.registration_success_window is not None: 
            self.registration_success_window.destroy() 
            self.registration_success_window = None 
 
        if self.meal_page_window is not None: 
            self.meal_page_window.destroy() 
            self.meal_page_window = None 
 
        if self.workout_page_window is not None: 
            self.workout_page_window.destroy() 
            self.workout_page_window = None 
 
        if self.fitness_dashboard_page_window is not None: 
            self.fitness_dashboard_page_window.destroy() 
            self.fitness_dashboard_page_window = None 
 
        if self.personalised_meal_planner_window is not None: 
            self.personalised_meal_planner_window.destroy() 
            self.personalised_meal_planner_window = None 
 
        if self.personalised_workout_planner_window is not None: 
            self.personalised_workout_planner_window.destroy() 
            self.personalised_workout_planner_window = None 
 
        if self.gym_features_window is not None: 
            self.gym_features_window.destroy() 
            self.gym_features_window = None 
 
        if self.gym_view_team_window is not None: 
            self.gym_view_team_window.destroy() 
            self.gym_view_team_window = None 
 
        if self.gym_classes_booking_window is not None: 
            self.gym_classes_booking_window.destroy() 
            self.gym_classes_booking_window = None 
 
        if self.gym_reviews_window is not None: 
            self.gym_reviews_window.destroy() 
            self.gym_reviews_window = None

 
196 
 
 
  
 
 
 
 
        if self.calculate_bmi_window is not None: 
            self.calculate_bmi_window.destroy() 
            self.calculate_bmi_window = None 
 
        if self.run_bmi_visualisation_window is not None: 
            self.run_bmi_visualisation_window.destroy() 
            self.run_bmi_visualisation_window = None 
 
        if self.view_member_class_schedule_window is not None: 
            self.view_member_class_schedule_window.destroy() 
            self.view_member_class_schedule_window = None 
 
        if self.view_member_class_clashes_window is not None: 
            self.view_member_class_clashes_window.destroy() 
            self.view_member_class_clashes_window = None 
 
        if self.class_reserve_slot_window is not None: 
            self.class_reserve_slot_window.destroy() 
            self.class_reserve_slot_window = None 
 
        if self.leave_class_window is not None: 
            self.leave_class_window.destroy() 
            self.leave_class_window = None 
 
        if self.update_profile_window is not None: 
            self.update_profile_window.destroy() 
            self.update_profile_window = None 
             
 
    def maximize_window(self, window): 
        screen_width = window.winfo_screenwidth() 
        screen_height = window.winfo_screenheight() 
 
        window.geometry(f"{screen_width}x{screen_height}+{-10}+{0}") 
 
if __name__ == "__main__": 
    manager = GymManager() 
    manager.run_home_page() 
 
    tk.mainloop() 

