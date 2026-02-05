import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from gym_function_bank import * 
from gym_font import * 
from PIL import Image, ImageTk 
from gym_user_dropdown_menu import * 
import math 
import datetime 
 
class GymClassBookingPage(tk.Tk): 
    def __init__(self, location_id, member_id, gym_features_callback, 
gym_view_team_callback, gym_class_booking_callback, gym_reviews_callback, 
gym_reserve_class_callback): 
        super().__init__() 
        self.title("Gym Class Booking") 
        self.geometry("800x600") 
        self.gym_page_menubar = GymPagesDropdownMenu(self, 
gym_features_callback, gym_view_team_callback, gym_class_booking_callback, 
gym_reviews_callback) 
        self.gym_reserve_class_callback = gym_reserve_class_callback 
 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
         
        self.location_id = location_id  
        self.member_id = member_id 
         
        self.get_location_id() 
 
        self.gym_page_menubar.pack(fill="x") 
 
        self.manage_font = ManageFont() 
 
        self.time_handler = TimeFormatHandler() 
 
        self.class_id = None 
 
        self.filter_classes = { 
            "classes": None, 
            "instructor": None, 
            "available_slots": None, 
        } 
 
        self.current_view = "grid" 
 
        self.current_date = datetime.date.today().strftime("%Y-%m-%d") 
        self.start_date = self.current_date 
 
        self.create_booking_page() 
         try: 
            end_date = self.calculate_end_date(self.start_date, 7) 
 
          filter_query = '''
              SELECT GymClasses.ClassID, GymClasses.ClassName,
                     Instructors.InstructorName, GymClasses.AvailableSlots,
                     ClassSchedule.StartTime, ClassSchedule.Duration, ClassSchedule.Date,
                     GymStudios.StudioName, ClassSchedule.Message
              FROM GymClasses
              JOIN Instructors ON GymClasses.InstructorID = Instructors.InstructorID
              JOIN ClassSchedule ON GymClasses.ClassID = ClassSchedule.ClassID
              JOIN GymStudios ON GymClasses.StudioID = GymStudios.StudioID
              WHERE Instructors.LocationID = ?
              AND ClassSchedule.Date BETWEEN ? AND ?
          '''
 
            filter_list = [self.location_id] 
             
            if self.filter_classes["classes"] != "All Classes" and 
self.filter_classes["classes"]: 
                filter_query += ' AND GymClasses.ClassName = ?' 
                filter_list.append(self.filter_classes["classes"]) 
 
            if self.filter_classes["instructor"] != "All Instructors" and 
self.filter_classes["instructor"]: 
                filter_query += ' AND Instructors.InstructorName = ?' 
                filter_list.append(self.filter_classes["instructor"]) 
 
            if self.filter_classes["available_slots"] != "All Slot 
Availabilities" and self.filter_classes["available_slots"]: 
                filter_query += ' AND GymClasses.AvailableSlots >= ?' 
                filter_list.append(self.filter_classes["available_slots"][:-1]) 
 
            day_preferences = {}   
 
            for day in self.day_checkboxes: 
                day_preferences[day] = self.day_checkboxes[day].get() 
 
            if any(day_preferences.values()): 
                days_to_filter = [] 
                for day in self.day_checkboxes: 
                    filtered_day = self.day_checkboxes[day].get() 
                    if filtered_day: 
                        
days_to_filter.append(str(list(self.day_checkboxes.keys()).index(day))) 
                days_str = ','.join(days_to_filter) 
    def fetch_gym_classes(self):
                      filter_query += f' AND CAST(strftime("%w", ClassSchedule.Date) 
AS INT) IN ({days_str})'  
 
            time_of_day_preferences = {}   
 
            for day in self.time_of_day_checkboxes: 
                time_of_day_preferences[day] = 
self.time_of_day_checkboxes[day].get() 
 
            if any(time_of_day_preferences.values()): 
                filter_query += ' AND (' 
                first_condition = True 
                index = 0 
                for time_of_day in self.time_of_day_checkboxes: 
                    index += 1 
                    filtered_time_of_day = time_of_day_preferences[time_of_day] 
                    if filtered_time_of_day: 
                        start_time_of_day = self.time_ranges[index-1][0] 
                        end_time_of_day = self.time_ranges[index-1][1] 
                        if not first_condition: 
                            filter_query += ' OR ' 
                        filter_query += f'(TIME(ClassSchedule.StartTime) BETWEEN 
"{start_time_of_day}" AND "{end_time_of_day}")' 
                        first_condition = False 
                filter_query += ')'  
         
            filter_query += ' ORDER BY ClassSchedule.Date, 
ClassSchedule.StartTime' 
 
            self.cursor.execute(filter_query, filter_list) 
            self.gym_classes = self.cursor.fetchall() 
    
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [] 
 
    def count_classes_per_day(self, date): 
        self.cursor.execute(''' 
            SELECT COUNT(GymClasses.ClassID) 
            FROM GymClasses 
            JOIN Instructors ON GymClasses.InstructorID = 
Instructors.InstructorID 
            JOIN ClassSchedule ON GymClasses.ClassID = ClassSchedule.ClassID 
            WHERE Instructors.LocationID = ? 
            AND ClassSchedule.Date = ? 
            GROUP BY ClassSchedule.Date 
        ''', (self.location_id, date)) 

        rows = self.cursor.fetchall() 
        class_count = [row[0] for row in rows][0] 
 
        return class_count 
         
    def class_filtering_option(self): 
        filter_frame = tk.Frame(self.scrollable_frame, background="#FFFFFF") 
        filter_frame.pack(fill='x', padx=10, pady=10) 
 
        ttk.Label(filter_frame, text="Find a Gym Class", width=145, 
background="#CCCCCC", 
font=self.manage_font.medium_bold_letters_font).pack(anchor=tk.W, padx=0) 
 
        filter_classes_frame = tk.Frame(filter_frame, background="#FFFFFF") 
        filter_classes_frame.pack(fill='x', padx=10, pady=10) 
 
        ttk.Label(filter_classes_frame, text="Filter Classes:", 
font=self.manage_font.medium_bold_heading_font, 
background="#FFFFFF").pack(side='left', padx=5) 
 
        classes = self.filter_class() 
        self.classes_var = tk.StringVar(value="All Classes") 
        classes_combo = ttk.Combobox(filter_classes_frame, 
textvariable=self.classes_var, values=["All Classes"] + classes) 
        classes_combo.pack(side='left', padx=5) 
        classes_combo.bind("<<ComboboxSelected>>", 
self.filter_classes_schedules) 
        classes_combo.config(font=self.manage_font.medium_bold_letters_font) 
         
        instructors = self.filter_instructors() 
        self.instructor_var = tk.StringVar(value="All Instructors") 
        instructor_combo = ttk.Combobox(filter_classes_frame, 
textvariable=self.instructor_var, values=["All Instructors"] + instructors) 
        instructor_combo.pack(side='left', padx=5) 
        instructor_combo.bind("<<ComboboxSelected>>", 
self.filter_classes_schedules) 
        instructor_combo.config(font=self.manage_font.medium_bold_letters_font) 
 
        available_slots = self.get_slots_left() 
        self.available_slots_var = tk.StringVar(value="All Slot Availabilities") 
        available_slots_combo = ttk.Combobox(filter_classes_frame, 
textvariable=self.available_slots_var, values=["All Slot Availabilities"] + 
[str(slot) + "+" for slot in available_slots]) 
        available_slots_combo.pack(side='left', padx=5) 
        available_slots_combo.bind("<<ComboboxSelected>>", 
self.filter_classes_schedules) 
        
available_slots_combo.config(font=self.manage_font.medium_bold_letters_font) 
 
        ttk.Separator(filter_frame, orient="horizontal", 
style="Custom.TSeparator").pack(fill="x", padx=10, pady=5) 
 
        day_preference_frame = tk.Frame(filter_frame, background="#FFFFFF") 
        day_preference_frame.pack(fill='x', padx=10, pady=10) 
 
        ttk.Label(day_preference_frame, text="Day Preference:", 
background="#FFFFFF", 
font=self.manage_font.medium_bold_heading_font).pack(side='left', anchor=tk.W, 
padx=5) 
        self.day_checkboxes = {} 
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
"Friday", "Saturday"] 
        for day in days_of_week: 
            var = tk.BooleanVar() 
            checkbox = tk.Checkbutton(day_preference_frame, text=day, 
variable=var, font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF", command=self.filter_classes_schedules) 
            checkbox.pack(side='left', padx=2) 
            self.day_checkboxes[day] = var 
 
        ttk.Separator(filter_frame, orient="horizontal", 
style="Custom.TSeparator").pack(fill="x", padx=10, pady=5) 
 
        time_of_day_preference_frame = tk.Frame(filter_frame, 
background="#FFFFFF") 
        time_of_day_preference_frame.pack(fill='x', padx=10, pady=10) 
 
        ttk.Label(time_of_day_preference_frame, text="Time of Day Preference:", 
font=self.manage_font.medium_bold_heading_font, 
background="#FFFFFF").pack(side='left', anchor=tk.W, padx=5) 
        self.time_of_day_checkboxes = {} 
        times_of_day = ["Morning", "Noon", "Afternoon", "Evening"] 
        self.time_ranges = [("6:00", "10:00"), ("10:00", "12:00"), ("12:00", 
"18:00"), ("18:00","21:00")] 
        index = 0 
        for time in times_of_day: 
            index += 1 
            var = tk.BooleanVar() 
            checkbox = tk.Checkbutton(time_of_day_preference_frame, 
text=f"{time}: {str(self.time_ranges[index-1][0])}-{str(self.time_ranges[index
1][1])}", variable=var, font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF", command=self.filter_classes_schedules) 
            checkbox.pack(side='left', padx=2) 
            self.time_of_day_checkboxes[time] = var 
 
        calendar_frame = tk.Frame(self.scrollable_frame, background="#FFFFFF")

        calendar_frame.pack(anchor=tk.W, padx=10, pady=10) 
 
        # Calendar button 
        self.continue_button = tk.Button(calendar_frame, text="Set Calendar", 
width=210, background="#333333", foreground="#FFFFFF", 
font=self.manage_font.small_bold_heading_font, 
command=self.open_calendar_window) 
        self.continue_button.pack(anchor=tk.W, padx=10, fill='both', pady=10) 
 
        # Grid and List button 
        grid_and_list_frame = tk.Frame(self.scrollable_frame, 
background="#FFFFFF") 
        grid_and_list_frame.pack(anchor=tk.W, padx=10, pady=10) 
         
        self.grid_button = tk.Button(grid_and_list_frame, text="Grid Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_grid_view) 
        self.grid_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E) 
 
        self.list_button = tk.Button(grid_and_list_frame, text="List Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_list_view) 
        self.list_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E) 
 
    def create_booking_page(self):      
        self.frame = ttk.Frame(self, style='TFrame') 
        self.frame.pack(fill='both', expand=True) 
 
        canvas = tk.Canvas(self.frame) 
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", 
command=canvas.yview) 
        self.scrollable_frame = ttk.Frame(canvas) 
 
        canvas.pack(side="left", fill="both", expand=True) 
        scrollbar.pack(side="right", fill="y") 
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        canvas.configure(yscrollcommand=scrollbar.set) 
 
        self.fetch_gym_location() 
 
        ttk.Label(self.scrollable_frame, text=f"Upcoming Gym Classes 
({self.gym_location})", width=135, background="#333333", foreground="#FFFFFF", 
font=self.manage_font.large_bold_heading_font).pack(anchor=tk.W, padx=10, 
pady=10) 
 
        class_information_frame = tk.Frame(self.scrollable_frame, width=50, 
background="#FFFFFF") 
        class_information_frame.pack(fill='both', expand=True) 
         
        gym_class_description = '''Are you ready to take your fitness journey to 
the next level? Your gym membership at FitZone provides exciting fitness classes 
and offers transformation like never before! \n 
Whether you're a beginner looking to kickstart a healthier lifestyle or a 
seasoned fitness member aiming to challenge your limits, our fitness classes 
caters to all levels and interests.''' 
         
        ttk.Label(class_information_frame, text=gym_class_description, 
width=135, background="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font).pack(anchor=tk.W, padx=10, 
pady=10) 
 
        ttk.Label(class_information_frame, text="Class enrollment is not guaranteed and is up to the decision of instructors.", width=135, 
background="#FFFFFF", 
font=self.manage_font.medium_underline_letters_font).pack(anchor=tk.W, padx=10, 
pady=10) 
 
        self.class_filtering_option() 
 
        button_frame = ttk.Frame(self.scrollable_frame, width=50, 
style='TFrame') 
        button_frame.pack(fill='both', expand=True) 
         
        prev_button = tk.Button(button_frame, text="Previous Week", 
command=self.go_to_previous_week, width=15, background="#CCCCCC", 
font=self.manage_font.small_bold_heading_font) 
        prev_button.grid(row=0, column=0, padx=10, pady=10, sticky="w") 
 
        button_spacing = tk.Label(button_frame, width=172) 
        button_spacing.grid(row=0, column=1, padx=10, pady=10, sticky="w") 
         
        next_button = tk.Button(button_frame, text="Next Week", 
command=self.go_to_next_week, width=15, background="#FFE4B5", 
font=self.manage_font.small_bold_heading_font) 
        next_button.grid(row=0, column=2, padx=10, pady=10, sticky="e") 
 
        self.scrollable_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
        
        self.create_timetable() 
 
        self.scrollable_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def create_timetable(self): 
        self.fetch_gym_classes() 

        self.classes_dict = {} 
 
        self.timetable_frame = ttk.Frame(self.scrollable_frame) 
        self.timetable_frame.pack(side="left", fill="y", padx=10, pady=10) 
 
        button_spacing = tk.Label(self.timetable_frame, text=f"From 
{self.start_date}", font=self.manage_font.medium_bold_letters_font, width=160) 
        button_spacing.pack(anchor="center", fill="both", padx=10, pady=10) 
 
        if not self.gym_classes: 
            tk.Label(self.timetable_frame, text="No classes scheduled for the selected week.", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
            tk.Label(self.timetable_frame, text="Try another day or", 
font=self.manage_font.smaller_letters_font).pack(anchor="center", fill="both", 
padx=10, pady=10) 
 
            message_label = tk.Button(self.timetable_frame, text="Reset Filters", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF", command=self.reset_filters) 
            message_label.pack(anchor="center", padx=10, pady=10) 
 
            ttk.Separator(self.timetable_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        for gym_class in self.gym_classes: 
            class_id, class_name, instructor, available_slots, start_time, 
duration, date, studio, message = gym_class 
 
            if date not in self.classes_dict: 
                self.classes_dict[date] = [] 
 
            self.classes_dict[date].append(gym_class) 
 
        if self.current_view == "grid": 
            self.create_grid_view() 
        elif self.current_view == "list": 
            self.create_list_view() 
 
    def create_grid_view(self): 
        for index in self.classes_dict: 
            classes = self.classes_dict[index] 
            date = index 
            date_frame = ttk.Frame(self.timetable_frame) 
            date_frame.pack(side="left", fill="y", padx=1, pady=10) 
 
            date_label = ttk.Label(date_frame, text=f"Date: {date}",
background="#333333", foreground="#FFFFFF", width=20, 
font=self.manage_font.medium_bold_heading_font) 
            date_label.pack(anchor=tk.W, padx=5, pady=10) 
 
            for gym_class in classes: 
                class_id, class_name, instructor, available_slots, start_time, 
duration, date, studio, message = gym_class 
 
                # Retrieve the slots left for this class based on its class ID 
                slots_left = self.get_slots_left().get(class_id, 0) 
 
                class_frame = tk.Frame(date_frame, background="#FFFFFF") 
                class_frame.pack(anchor=tk.W, padx=5, pady=10) 
 
                ttk.Label(class_frame, text=class_name, background="#FFFFFF", 
width=20, font=self.manage_font.medium_bold_heading_font).pack(anchor=tk.W) 
 
                end_time = self.time_handler.calculate_end_time(start_time, 
duration) 
                start_time_str = self.time_handler.convert_to_am_pm(start_time) 
                schedule_label = f"Schedule: {start_time_str} - \n {end_time}" 
                ttk.Label(class_frame, text=schedule_label, 
background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
 
                instructor_label = f"Instructor: {instructor}" 
                ttk.Label(class_frame, text=instructor_label, 
background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
 
                slots_label = f"Available Slots: {slots_left}" 
                ttk.Label(class_frame, text=slots_label, background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
 
                book_button = tk.Button(class_frame, text="Book Class", 
width=15, background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font, command=lambda class_id=class_id: 
self.set_class_id(class_id)) 
                book_button.pack(anchor=tk.W, padx=10, pady=10) 
 
                if not self.is_date_after_current_date(date, start_time) or 
slots_left <= 0: 
                    book_button.config(state=tk.DISABLED) 
 
    def set_class_id(self, class_id): 
        self.class_id = class_id 
        self.gym_reserve_class_callback()

    def create_list_view(self): 
        for index in self.classes_dict: 
            classes = self.classes_dict[index] 
            date = index 
            date_frame = ttk.Frame(self.timetable_frame) 
            date_frame.pack(padx=0, pady=0) 
 
            date_label = tk.Label(date_frame, text=f"Date: {date}", width=190, 
font=self.manage_font.medium_bold_heading_font, background="#333333", 
foreground="#FFFFFF") 
            date_label.pack(anchor="center", pady=0) 
 
            style=ttk.Style() 
            style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
            columns = ["Class Name", "Schedule", "Instructor", "Available Slots", "Studio", "Message"] 
            list_view = ttk.Treeview(date_frame, style="Custom.Treeview", 
height=self.count_classes_per_day(date)+1) 
            list_view.pack(fill="both", expand=True) 
 
            list_view["columns"] = columns 
            list_view.heading("#1", text="Class Name") 
            list_view.heading("#2", text="Schedule") 
            list_view.heading("#3", text="Instructor") 
            list_view.heading("#4", text="Available Slots") 
            list_view.heading("#5", text="Studio") 
            list_view.heading("#6", text="Message") 
 
            for gym_class in classes: 
                class_id, class_name, instructor, available_slots, start_time, 
duration, date, studio, message = gym_class 
                end_time = self.calculate_end_time(start_time, duration) 
                list_view.insert("", "end", values=[class_name, f"{start_time} - 
{end_time}", instructor, available_slots, studio, message]) 
 
    def show_grid_view(self): 
        self.current_view = "grid" 
 
        self.refresh_timetable() 
 
    def show_list_view(self):  
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
        self.current_view = "list" 
        self.refresh_timetable() 
 
    def is_date_after_current_date(self, date, start_time): 
        input_datetime = datetime.datetime.strptime(f"{date} {start_time}", '%Y
%m-%d %H:%M') 
        current_datetime = datetime.datetime.now() 
 
        return input_datetime > current_datetime 
 
    def go_to_previous_week(self): 
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        start_date = start_date - datetime.timedelta(days=7) 
        start_date = start_date.strftime('%Y-%m-%d') 
        self.start_date = str(start_date) 
 
        self.refresh_timetable() 
 
    def go_to_next_week(self): 
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        start_date = start_date + datetime.timedelta(days=7) 
        start_date = start_date.strftime('%Y-%m-%d') 
        self.start_date = str(start_date) 
 
        self.refresh_timetable() 
 
    def calculate_end_date(self, start_date, days): 
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') 
        end_date = start_date + datetime.timedelta(days=days) 
        end_date_str = end_date.strftime('%Y-%m-%d') 
        return end_date_str 
 
    def filter_instructors(self): 
        try: 
            self.cursor.execute("SELECT DISTINCT InstructorName FROM Instructors") 
            instructors = [row[0] for row in self.cursor.fetchall()] 
 
            return instructors 
             
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [] 
 
    def filter_class(self): 
        try: 
            self.cursor.execute("SELECT DISTINCT ClassName FROM GymClasses")
            classes = [row[0] for row in self.cursor.fetchall()] 
 
            return classes 
             
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [] 
 
    def fetch_gym_location(self): 
        try: 
            self.cursor.execute("SELECT LocationName FROM GymLocations WHERE LocationID=?", (self.location_id,)) 
            self.gym_location = self.cursor.fetchone()[0] 
 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None         
 
    def filter_classes_schedules(self, event=None): 
        if self.classes_var.get() != "All": 
            self.filter_classes["classes"] = self.classes_var.get() 
        else: 
            self.filter_classes["classes"] = None 
             
        if self.instructor_var.get() != "All": 
            self.filter_classes["instructor"] = self.instructor_var.get() 
        else: 
            self.filter_classes["instructor"] = None 
             
        if self.available_slots_var.get() != "All": 
            self.filter_classes["available_slots"] = 
self.available_slots_var.get() 
        else: 
            self.filter_classes["available_slots"] = None 
         
        self.refresh_timetable() 
 
    def get_slots_left(self): 
        try: 
            self.cursor.execute("SELECT GymClasses.ClassID, 
GymClasses.AvailableSlots, COUNT(Enrollment.EnrollmentID) as EnrolledCount "  
                                "FROM GymClasses " 
                                "LEFT JOIN Enrollment ON GymClasses.ClassID = 
Enrollment.ClassID " 
                                "GROUP BY GymClasses.ClassID") 
             
            slots_left_data = self.cursor.fetchall() 

            # Create a dictionary to store the slots left for each class ID 
            slots_left_dict = {class_id: available_slots - enrolled_count for 
class_id, available_slots, enrolled_count in slots_left_data} 
             
            return slots_left_dict 
                 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return {} 
 
 
    def refresh_timetable(self): 
        try: 
            self.timetable_frame.destroy() 
        except: 
            None 
        self.create_timetable() 
 
 
    def reset_filters(self): 
        self.filter_classes = { 
            "classes": None, 
            "instructor": None, 
            "available_slots": None, 
        } 
 
        self.start_date = datetime.date.today().strftime("%Y-%m-%d") 
        self.day_checkboxes = {} 
 
        self.time_of_day_checkboxes = {} 
 
        self.refresh_timetable() 
 
 
    def get_location_id(self): 
        if self.member_id: 
            self.cursor.execute(''' 
                SELECT LocationID 
                FROM Members 
                WHERE MemberID = ?; 
            ''', (self.member_id,)) 
            location_id = self.cursor.fetchone() 
 
            if location_id: 
                self.location_id = location_id[0] 
 
    def calculate_end_time(self, start_time, duration): 
        start_time = datetime.datetime.strptime(start_time, "%H:%M")
        duration_hours, duration_minutes = map(int, duration.split(':')) 
        duration_timedelta = datetime.timedelta(hours=duration_hours, 
minutes=duration_minutes) 
        end_time = start_time + duration_timedelta 
        end_time_str = end_time.strftime("%H:%M") 
         
        return end_time_str 
         
    def open_calendar_window(self): 
        calendar_window = CalendarWindow(self, "View Date") 
 
    def update_start_date(self, selected_date): 
        self.start_date = selected_date 
        self.refresh_timetable() 
 
    def get_class_id(self): 
        return self.class_id 
 
if __name__ == "__main__": 
    GymClassBookingPage(1, None, None, None, None, None, None).mainloop()
