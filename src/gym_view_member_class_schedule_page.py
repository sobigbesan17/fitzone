import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from gym_function_bank import * 
from gym_font import * 
from gym_user_dropdown_menu import * 
import datetime 
 
class MemberClassSchedulePage(tk.Tk): 
    def __init__(self, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
                 gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback, 
leave_class_schedule_callback): 
        super().__init__() 
        self.title("Member Class Schedule") 
        self.geometry("800x600") 
 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.manage_font = ManageFont() 
 
        self.time_handler = TimeFormatHandler() 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, 
                                                      
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback) 
        self.leave_class_schedule_callback = leave_class_schedule_callback 
         
        self.gym_class_booking_callback = gym_class_booking_callback 
         
        self.user_dropdown_menu.pack(fill="x")  
 
        self.current_view = "grid" 
 
        self.current_sorting = "date" 
 
        self.member_id = member_id 
        self.class_schedule_id = None 
 
        self.get_location_id() 
        self.current_date = datetime.date.today().strftime("%Y-%m-%d") 
        self.start_date = self.current_date 
 
        self.create_schedule_page() 
 
    def fetch_member_schedule(self): 
        try: 
            end_date = self.calculate_end_date(self.start_date, 7) 
 
            filter_query = '''
    SELECT GymClasses.ClassID, GymClasses.ClassName,
           Instructors.InstructorName,
           ClassSchedule.ScheduleID, GymClasses.AvailableSlots,
           ClassSchedule.StartTime, ClassSchedule.Duration, ClassSchedule.Date,
           GymStudios.StudioName, ClassSchedule.Message
    FROM GymClasses
    JOIN Instructors ON GymClasses.InstructorID = Instructors.InstructorID
    JOIN ClassSchedule ON GymClasses.ClassID = ClassSchedule.ClassID
    JOIN GymStudios ON GymClasses.StudioID = GymStudios.StudioID
    JOIN Enrollment ON GymClasses.ClassID = Enrollment.ClassID
    WHERE Enrollment.MemberID = ?
    AND ClassSchedule.Date BETWEEN ? AND ? '''

            self.cursor.execute(filter_query, (self.member_id, self.start_date, end_date))
            self.member_schedule = self.cursor.fetchall()

        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [] 
     
    def create_schedule_page(self): 
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
 
        ttk.Label(self.scrollable_frame, text="Your Class Schedule", width=135, 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.large_bold_heading_font).pack(anchor=tk.W, padx=10, 
pady=10) 
 
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
 
        self.create_schedule_view() 
 
        self.scrollable_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def create_schedule_view(self): 
        self.fetch_member_schedule() 
 
        button_spacing = tk.Label(self.scrollable_frame, text=f"From {self.start_date}", font=self.manage_font.medium_bold_letters_font, width=160) 
        button_spacing.pack(anchor="center", fill="both", padx=10, pady=10) 
 
        if not self.member_schedule: 
            tk.Label(self.scrollable_frame, text="No classes booked for the selected week.", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
            tk.Label(self.scrollable_frame, text="Try another day or", 
font=self.manage_font.smaller_letters_font).pack(anchor="center", fill="both", 
padx=10, pady=10) 
 
            message_label = tk.Button(self.scrollable_frame, text="Enroll Class", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF", command=self.gym_class_booking_callback) 
            message_label.pack(anchor="center", padx=10, pady=10) 
 
            ttk.Separator(self.scrollable_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        if self.current_view == "grid": 
            self.create_grid_view() 
        elif self.current_view == "list": 
            self.create_list_view() 
 
    def create_grid_view(self): 
        grid_dict = {} 
         
        grid_frame = ttk.Frame(self.scrollable_frame, style='TFrame') 
        grid_frame.pack(anchor=tk.W, padx=10, pady=10) 
         
        for gym_class in self.member_schedule:
            class_id, class_name, instructor, class_schedule_id, available_slots, start_time, duration, date, studio, message = gym_class 
 
            if date not in grid_dict: 
                grid_dict[date] = [] 
 
            grid_dict[date].append(gym_class) 
 
        column = 0 
        for date, classes in grid_dict.items(): 
            date_frame = ttk.Frame(grid_frame, style='TFrame') 
            date_frame.grid(row=0, column=column, padx=1, pady=10, sticky="n") 
            column += 1 
 
            ttk.Label(date_frame, text=f"Date: {date}", background="#333333", 
foreground="#FFFFFF", width=20, 
font=self.manage_font.medium_bold_heading_font).pack(anchor=tk.W, padx=5, 
pady=10) 
 
            for gym_class in classes: 
                class_id, class_name, instructor, class_schedule_id, available_slots, start_time, duration, date, studio, message = gym_class 
 
                class_frame = tk.Frame(date_frame, background="#FFFFFF") 
                class_frame.pack(anchor=tk.W, padx=5, pady=10) 
 
                ttk.Label(class_frame, text=class_name, background="#FFFFFF", 
width=20, font=self.manage_font.medium_bold_heading_font).pack(anchor=tk.W) 
 
                end_time = self.time_handler.calculate_end_time(start_time, 
duration) 
 
                start_time = self.time_handler.convert_to_am_pm(start_time) 
 
                schedule_label = f"Schedule: {start_time} - \n {end_time}" 
                ttk.Label(class_frame, text=schedule_label, 
background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
 
                instructor_label = f"Instructor: {instructor}" 
                ttk.Label(class_frame, text=instructor_label, 
background="#FFFFFF", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
 
                leave_button = tk.Button(class_frame, text="leave Class", 
width=15, background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font, command=lambda 
class_schedule_id=class_schedule_id: self.leave_class(class_schedule_id))

                leave_button.pack(anchor=tk.W, padx=10, pady=10) 
                 
    def create_list_view(self): 
        self.classes_dict = {} 
 
        list_frame = ttk.Frame(self.scrollable_frame, style='TFrame') 
        list_frame.pack(anchor=tk.W, padx=10, pady=10) 
         
        for gym_class in self.member_schedule: 
            class_id, class_name, instructor, class_schedule_id, available_slots, start_time, duration, date, studio, message = gym_class 
 
            if date not in self.classes_dict: 
                self.classes_dict[date] = [] 
 
            self.classes_dict[date].append(gym_class) 
         
        for index in self.classes_dict: 
            classes = self.classes_dict[index] 
            date = index 
            date_frame = ttk.Frame(list_frame) 
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
                class_id, class_name, instructor, class_schedule_id, available_slots, start_time, duration, date, studio, message = gym_class 
                 
                end_time = self.time_handler.calculate_end_time(start_time, 
duration) 
                start_time = self.time_handler.convert_to_am_pm(start_time) 
                 
                list_view.insert("", "end", values=[class_name, f"{start_time} - {end_time}", instructor, available_slots, studio, message]) 
 
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
 
    def calculate_end_date(self, start_date, days): 
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') 
        end_date = start_date + datetime.timedelta(days=days) 
        end_date_str = end_date.strftime('%Y-%m-%d') 
        return end_date_str 
 
    def go_to_previous_week(self): 
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        start_date = start_date - datetime.timedelta(days=7) 
        start_date = start_date.strftime('%Y-%m-%d') 
        self.start_date = str(start_date) 
         
        if self.current_view == "grid": 
            self.show_grid_view() 
        else: 
            self.show_list_view() 
 
    def go_to_next_week(self): 
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d') 
        start_date = start_date + datetime.timedelta(days=7) 
        start_date = start_date.strftime('%Y-%m-%d') 
        self.start_date = str(start_date) 

        if self.current_view == "grid": 
            self.show_grid_view() 
        else: 
            self.show_list_view() 
 
    def show_grid_view(self): 
        self.current_view = "grid" 
        self.frame.destroy() 
        self.create_schedule_page() 
 
    def show_list_view(self): 
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
        self.current_view = "list" 
        self.frame.destroy() 
        self.create_schedule_page() 
 
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
 
    def leave_class(self, class_schedule_id): 
        self.class_schedule_id = class_schedule_id 
        if self.leave_class_schedule_callback: 
            self.leave_class_schedule_callback() 
 
    def get_class_schedule_id(self): 
        return self.class_schedule_id 
