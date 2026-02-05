import tkinter as tk 
from tkinter import ttk
import sqlite3 
from gym_function_bank import * 
from gym_user_dropdown_menu import * 
from gym_font import * 
 
class ModifyClassPage(tk.Tk): 
    def __init__(self, class_schedule_id, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
                 gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback): 
        super().__init__() 
        self.title("Modify Class") 
        self.geometry("800x600") 
 
        self.class_schedule_id = class_schedule_id 
 
        class_id = None 
 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.current_date = datetime.date.today() 
 
        self.time_handler = TimeFormatHandler() 
 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, 
                                                      
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback) 
 
        self.manage_font = ManageFont() 
 
        self.message_handler = MessageHandler(self) 
 
        self.user_dropdown_menu.pack(fill="x")  
 
        self.canvas = tk.Canvas(self, background="white") 
        self.canvas.pack(fill="both", expand=True) 
 
        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", 
command=self.canvas.yview) 
        self.scrollbar.pack(side="right", fill="y") 
 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.bind("<Configure>", self.configure_canvas)
          self.content_frame = tk.Frame(self.canvas) 
        self.canvas.create_window((0, 0), window=self.content_frame, 
anchor="nw") 
 
        self.error_string = None 
        self.success_string = None 
 
        self.create_modify_class_page() 
 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def configure_canvas(self, event): 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def find_linked_classes_schedules(self): 
        try: 
            class_id_query = "SELECT ClassID FROM ClassSchedule WHERE ScheduleID 
= ?" 
            self.cursor.execute(class_id_query, (self.class_schedule_id,)) 
            self.class_id_result = self.cursor.fetchone() 
 
            if self.class_id_result: 
                class_id = self.class_id_result[0] 
             
                linked_classes_query = ''' 
                SELECT GymClasses.ClassName, Instructors.InstructorName,  
                ClassSchedule.StartTime, ClassSchedule.Duration, 
ClassSchedule.Date, 
                GymStudios.StudioName, ClassSchedule.Message 
                FROM GymClasses 
                JOIN Instructors ON GymClasses.InstructorID = 
Instructors.InstructorID 
                JOIN ClassSchedule ON GymClasses.ClassID = ClassSchedule.ClassID 
                JOIN GymStudios ON GymClasses.StudioID = GymStudios.StudioID 
                WHERE GymClasses.ClassID = ? AND ClassSchedule.Date >= ? 
                ''' 
             
                self.cursor.execute(linked_classes_query, (class_id, 
self.current_date)) 
                linked_classes = self.cursor.fetchall() 
             
                return linked_classes 
            else: 
                return None 
             
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None   
 
    def fetch_enrollment_details(self): 
        try: 
            query = ''' 
            SELECT GymClasses.ClassID, GymClasses.ClassName, 
Instructors.InstructorName,  
            ClassSchedule.StartTime, ClassSchedule.Duration, ClassSchedule.Date,  
            GymStudios.StudioName, ClassSchedule.Message 
            FROM Enrollment 
            JOIN GymClasses ON ClassSchedule.ClassID = GymClasses.ClassID 
            JOIN Instructors ON GymClasses.InstructorID = 
Instructors.InstructorID 
            JOIN ClassSchedule ON GymClasses.ClassID = ClassSchedule.ClassID 
            JOIN GymStudios ON GymClasses.StudioID = GymStudios.StudioID 
            WHERE ClassSchedule.ScheduleID = ? 
            ''' 
 
            self.cursor.execute(query, (self.class_schedule_id,)) 
            enrollment_details = self.cursor.fetchone() 
            return enrollment_details 
 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None 
 
    def create_modify_class_page(self): 
        enrollment_details = self.fetch_enrollment_details() 
 
        if not enrollment_details: 
            tk.Label(self.content_frame, text="Class schedule not found.", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
            return 
 
        ttk.Label(self.content_frame, text="Leave Class", 
font=self.manage_font.heading_font).pack(anchor=tk.W, padx=10, pady=10) 
 
        leaving_gym_class_sentence = '''\tBefore leaving a gym class, please 
check the dates and times of the remaining classes in your schedule:''' 
 
        ttk.Label(self.content_frame, text=leaving_gym_class_sentence, 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W, padx=10, pady=10) 
 
        index = 0 
         
        grid_frame = tk.Frame(self.content_frame) 
        grid_frame.pack(anchor=tk.W, padx=10, pady=10)
        for class_schedule in self.find_linked_classes_schedules(): 
            row = index // 5 
            column = index % 5 
            class_name, instructor, start_time, duration, date, studio, message 
= class_schedule 
 
            class_frame = tk.Frame(grid_frame, background="#FFFFFF") 
            class_frame.grid(row=row, column=column, padx=10, pady=10) 
 
            ttk.Label(class_frame, text=f"Date: {date}", background="#333333", 
foreground="#FFFFFF", width=27, 
font=self.manage_font.medium_bold_heading_font).pack(anchor=tk.W, fill="x") 
 
            ttk.Label(class_frame, text="Class Schedule:", background="#FFFFFF", 
width=20, font=self.manage_font.medium_bold_letters_font).pack(anchor="w", 
padx=10, pady=10) 
             
            ttk.Separator(class_frame, orient="horizontal").pack(fill="x", 
padx=10, pady=10) 
             
            ttk.Label(class_frame, text=class_name, background="#FFFFFF", 
font=self.manage_font.small_bold_heading_font).pack(anchor="w", padx=10, 
pady=10) 
             
            end_time = self.time_handler.calculate_end_time(start_time, 
duration) 
 
            start_time_str = self.time_handler.convert_to_am_pm(start_time) 
             
            schedule_label = f"Schedule: {start_time_str} - {end_time}" 
            ttk.Label(class_frame, text=schedule_label, background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor="w", padx=10, pady=10) 
             
            instructor_label = f"Instructor: {instructor}" 
            ttk.Label(class_frame, text=instructor_label, background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor="w", padx=10, pady=10) 
             
            studio_label = f"Studio: {studio}" 
            ttk.Label(class_frame, text=studio_label, background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor="w", padx=10, pady=10) 
 
            message_frame = tk.Frame(class_frame, background="#666666") 
            message_frame.pack(anchor=tk.W) 
 
            ttk.Label(message_frame, text="Message:", background="#666666", 
width=20, font=self.manage_font.medium_bold_letters_font).pack(anchor="w", 
padx=10) 
            message_label = tk.Label(message_frame, text=message, background="#666666", font=self.manage_font.medium_letters_font, wraplength=600) 
            message_label.pack(anchor="w", padx=10) 
 
            index += 1 
 
        file_path = 'gym_leaving_class.txt' 
 
        with open(file_path, 'r') as file: 
            leaving_gym_class_message = file.read() 
 
        ttk.Label(self.content_frame, text=leaving_gym_class_message, 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W, padx=10, pady=10) 
 
        leave_class_button = tk.Button(self.content_frame, text="Leave Class", 
background="#8B0000", foreground="#FFFFFF", 
font=self.manage_font.small_bold_heading_font, command=self.leave_class) 
        leave_class_button.pack(anchor="center", padx=10, pady=30) 
 
    def find_class_id_from_schedule_id(self, schedule_id): 
        try: 
            query = "SELECT ClassID FROM ClassSchedule WHERE ScheduleID = ?" 
            self.cursor.execute(query, (schedule_id,)) 
            result = self.cursor.fetchone() 
            if result: 
                class_id = result[0] 
                return class_id 
            else: 
                return None  # Return None if the Schedule ID doesn't exist 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None  # Return None in case of an error 
 
    def leave_class(self): 
        try: 
            class_id = 
self.find_class_id_from_schedule_id(self.class_schedule_id) 
             
            self.cursor.execute("DELETE FROM Enrollment WHERE ClassID = ?", 
(class_id,)) 
            self.conn.commit() 
            self.success_string = "Success: \n\n \u2705 Class has been removed 
from your schedule." 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            error_string = "Error: \n\n \u26A0 Failed to leave the class." 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string)
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
 
if __name__ == "__main__": 
    ModifyClassPage(7, 1, None, None, None, None, None, None, None, 
None).mainloop()
