import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from gym_function_bank import * 
from PIL import Image, ImageTk 
from gym_user_dropdown_menu import * 
import math 
import datetime 
 
class GymClassReservationPage(tk.Tk): 
    def __init__(self, class_id, member_id, gym_features_callback, 
gym_view_team_callback, gym_class_booking_callback, gym_reviews_callback): 
        super().__init__() 
        self.title("Gym Class Reservation") 
        self.geometry("800x600") 
        self.gym_page_menubar = GymPagesDropdownMenu(self, 
gym_features_callback, gym_view_team_callback, gym_class_booking_callback, 
gym_reviews_callback) 
        self.gym_class_booking_callback = gym_class_booking_callback 
 
        self.enrollment_count = None
   
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.manage_font = ManageFont() 
        self.message_handler = MessageHandler(self) 
 
        self.current_date = datetime.date.today().strftime("%Y-%m-%d") 
        self.gym_page_menubar.pack(fill="x") 
 
        self.class_id = class_id 
        self.member_id = member_id 
         
        self.get_class_info_by_id() 
 
        self.create_reservations_page() 
             
    def create_reservations_page(self): 
        earliest_class_date = self.get_earliest_future_date_for_class() 
 
        if earliest_class_date: 
            class_name_label = tk.Label(self, text=f"Starting from {earliest_class_date}", font=self.manage_font.large_bold_heading_font) 
            class_name_label.pack(padx=10, pady=5, anchor="center") 
             
        if self.class_info: 
            self.class_info_frame = tk.Frame(self, background="#333333") 
            self.class_info_frame.pack(padx=10, pady=10) 
 
            class_name_label = tk.Label(self.class_info_frame, 
text=self.class_name, font=self.manage_font.large_bold_heading_font, 
background="#333333", foreground="#FFE4B5") 
            class_name_label.pack(padx=10, pady=5, anchor="w") 
 
            close_button = tk.Button(self.class_info_frame, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.gym_class_booking_callback) 
            close_button.place(relx=1, rely=0, anchor="ne") 
 
            self.enrollment_count = self.get_enrollment_count() 
 
            number_of_members_label = tk.Label(self.class_info_frame, 
text=f"Number Of Enrolled Members: {self.enrollment_count}", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF") 
            number_of_members_label.pack(padx=10, pady=5, anchor="w") 
 
            number_of_members_label = tk.Label(self.class_info_frame, 
text=f"Average Rating: {self.enrollment_count}", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF") 
            number_of_members_label.pack(padx=10, pady=5, anchor="w")         
 
            self.create_reservations_table() 
 
            is_enrolled = self.check_member_enrollment() 
 
            if is_enrolled: 
                self.enroll_class_button = tk.Button(self.class_info_frame, 
text="Already Enrolled", font=self.manage_font.medium_bold_heading_font, 
width=150, background="#FF5733", state="disabled") 
            else: 
                self.enroll_class_button = tk.Button(self.class_info_frame, 
text="Enroll Class", font=self.manage_font.medium_bold_heading_font, width=150, 
background="#FFE4B5", command=self.enroll_member_in_class) 
             
            self.enroll_class_button.pack(padx=10, pady=5) 
        else: 
            tk.Label(self, text="Class not found.", 
font=self.manage_font.medium_bold_heading_font, width=70, 
background="#FFE4B5").pack(padx=10, pady=10) 
 
    def create_reservations_table(self): 
        style = ttk.Style() 
        style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
        style.configure("Custom.Treeview", borderwidth=1, relief="solid", 
font=self.manage_font.medium_bold_letters_font)   
 
        columns = ["Class Name", "Available Slots Left", "Instructor"] 
 
        list_view = ttk.Treeview(self.class_info_frame, style="Custom.Treeview", 
height=4) 
        list_view.pack(fill="both", expand=True) 
 
        list_view["columns"] = columns 
        list_view.heading("#1", text="Class Name") 
        list_view.heading("#2", text="Available Slots Left") 
        list_view.heading("#3", text="Instructor") 
 
        list_view.insert("", "end", values=[self.class_name, 
self.available_slots - self.enrollment_count, self.instructor_name]) 
 
    def enroll_member_in_class(self): 
        success_message = None 
        error_message = None 
         
        if self.member_id is None: 
            return 
 
        try: 
            if self.available_slots > 0: 
                print(self.member_id, self.class_id) 
                # Enrolls the member into the class 
                self.cursor.execute(''' 
                    INSERT INTO Enrollment (MemberID, ClassID) 
                    VALUES (?, ?) 
                ''', (self.member_id, self.class_id)) 
 
                self.conn.commit() 
 
                self.enroll_class_button.configure(state="disabled") 
 
                success_message = "Success: \n\n \u2705 Enrollment successful! You will be redirected shortly." 
            else: 
                error_message = "Error: \n\n \u26A0 Enrollment unsucessful!" 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
        finally: 
            if error_message: 
                self.message_handler.invalid_message(error_string) 
            else: 
                self.message_handler.success_message(success_message) 
                self.after(3000, self.perform_success) 
 
    def get_class_info_by_id(self): 
        self.cursor.execute(''' 
            SELECT GymClasses.ClassName, GymClasses.AvailableSlots, 
Instructors.InstructorName 
            FROM GymClasses 
            INNER JOIN ClassSchedule ON GymClasses.ClassID = 
ClassSchedule.ClassID 
            INNER JOIN Instructors ON GymClasses.InstructorID = 
Instructors.InstructorID   
            WHERE GymClasses.ClassID = ? 
        ''', (self.class_id,)) 
        self.class_info = self.cursor.fetchall() 
        for row in self.class_info: 
            self.class_name, self.available_slots, self.instructor_name = row 
 
    def get_enrollment_count(self): 
        self.cursor.execute(''' 
            SELECT COUNT(*)
            FROM Enrollment 
            WHERE ClassID = ? 
        ''', (self.class_id,)) 
        enrollment_count = self.cursor.fetchone()[0] 
        return enrollment_count 
 
    def get_earliest_future_date_for_class(self): 
        self.cursor.execute(''' 
            SELECT MIN(ClassSchedule.Date) 
            FROM GymClasses 
            INNER JOIN ClassSchedule ON GymClasses.ClassID = 
ClassSchedule.ClassID 
            WHERE GymClasses.ClassID = ? AND ClassSchedule.Date >= ? 
        ''', (self.class_id, self.current_date)) 
        earliest_class_date = self.cursor.fetchone()[0] 
        return earliest_class_date 
 
    def check_member_enrollment(self): 
        if self.member_id is None: 
            return False 
 
        try: 
            # Check if the member is already enrolled in the class 
            self.cursor.execute(''' 
                SELECT COUNT(*)  
                FROM Enrollment 
                WHERE MemberID = ? AND ClassID = ? 
            ''', (self.member_id, self.class_id)) 
            enrollment_count = self.cursor.fetchone()[0] 
 
            return enrollment_count > 0 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return False 
 
    def perform_success(self): 
        self.enroll_class_button.bind("<Button-1>", lambda event, 
func=self.gym_class_booking_callback: func()) 
        self.enroll_class_button.event_generate("<Button-1>") 
 
if __name__ == "__main__": 
    GymClassReservationPage(1, 3, None, None, None, None).mainloop()
