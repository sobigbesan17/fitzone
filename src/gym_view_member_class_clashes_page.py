import sqlite3 
from datetime import datetime, timedelta 
import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox 
from gym_font import * 
from gym_function_bank import * 
from gym_user_dropdown_menu import * 
 
class MemberClassClashesPage(tk.Tk): 
    def __init__(self, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback, 
modify_class_schedule_callback): 
        super().__init__() 
        self.title("Upcoming Class Schedules") 
        self.geometry("1200x800") 
 
        self.member_id = member_id 
        self.current_datetime = datetime.datetime.now() 
         
        self.manage_font = ManageFont() 
 
        self.message_handler = MessageHandler(self) 
 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, gym_workout_planner_callback, 
view_class_schedule_callback, gym_class_booking_callback, 
gym_class_clashes_callback) 
         
        self.user_dropdown_menu.pack(fill="x") 
         
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.load_class_schedules() 
 
    def load_class_schedules(self): 
        self.cursor.execute(f""" 
            SELECT GymClasses.ClassName, Instructors.InstructorName, 
ClassSchedule.StartTime, ClassSchedule.Date, ClassSchedule.Duration 
            FROM Enrollment 
            JOIN ClassSchedule ON Enrollment.ClassID = ClassSchedule.ClassID 
            JOIN GymClasses ON Enrollment.ClassID = GymClasses.ClassID 
            JOIN Instructors ON GymClasses.InstructorID = 
Instructors.InstructorID
            WHERE Enrollment.MemberID = {self.member_id} 
        """) 
        rows = self.cursor.fetchall() 
 
        distinct_schedules = {} 
        for row1 in rows: 
            for row2 in rows: 
                if row1 == row2: 
                    continue 
 
                start_time1, date1, duration1 = row1[2], row1[3], row1[4] 
                start_time2, date2, duration2 = row2[2], row2[3], row2[4] 
 
                if None in (start_time1, duration1, start_time2, duration2): 
                    continue 
 
                end_time1 = self.calculate_end_time(start_time1, duration1) 
                end_time2 = self.calculate_end_time(start_time2, duration2) 
 
                date1_datetime = datetime.datetime.strptime(date1, "%Y-%m-%d") 
                date2_datetime = datetime.datetime.strptime(date2, "%Y-%m-%d") 
 
                if date1_datetime > self.current_datetime and date2_datetime > self.current_datetime: 
                    if date1 == date2 and start_time1 < end_time2 and start_time2 < end_time1: 
                        if (row1, row2) not in distinct_schedules.values() and (row2, row1) not in distinct_schedules.values(): 
                            distinct_schedules[len(distinct_schedules) + 1] = (row1, row2) 
 
        self.sorted_schedules = sorted(distinct_schedules.values(), key=lambda x: (x[0][3], x[0][2])) 
 
        if not self.sorted_schedules: 
            self.title_frame = ttk.Label(self, text="Current Class Clashes:", 
font=self.manage_font.large_bold_heading_font, background="#333333", 
foreground="#FFFFFF") 
            self.title_frame.pack(fill="x") 
 
            tk.Label(self, text="No current class clashes found.", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
        else: 
            self.display_class_clashes() 
 
    def calculate_end_time(self, start_time, duration): 
        if start_time is None or duration is None:
            return None 
         
        start_time_obj = datetime.datetime.strptime(start_time, "%H:%M") 
        duration_obj = datetime.datetime.strptime(duration, "%H:%M") 
        end_time_obj = start_time_obj + timedelta(hours=duration_obj.hour, 
minutes=duration_obj.minute) 
        return end_time_obj.strftime("%H:%M") 
 
    def display_class_clashes(self): 
        self.canvas = tk.Canvas(self) 
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
 
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, 
command=self.canvas.yview) 
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
 
        self.tree_frame = ttk.Frame(self.canvas) 
        self.canvas.create_window((0, 0), window=self.tree_frame, anchor=tk.NW) 
 
        # Group overlapping schedules with two or more clashes 
        grouped_schedules = [] 
        current_date = None 
        current_group = [] 
 
        self.title_frame = ttk.Label(self.tree_frame, text="Cureent Class Clashes:", font=self.manage_font.large_bold_heading_font, background="#333333", 
foreground="#FFFFFF") 
        self.title_frame.pack(fill="x") 
 
        for row1, row2 in self.sorted_schedules: 
            date = row1[3] 
            if date != current_date: 
                if current_group: 
                    grouped_schedules.append((current_date, current_group)) 
                current_date = date 
                current_group = [(row1, row2)] 
            else: 
                current_group.append((row1, row2)) 
 
        if current_group: 
            grouped_schedules.append((current_date, current_group)) 
             
        for index, (date, rows) in enumerate(grouped_schedules, start=1): 
            if index > 1: 
                ttk.Separator(self.tree_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
            self.create_treeview(date, rows) 
             
        self.tree_frame.bind("<Configure>", self.on_frame_configure) 
 
        # Closing the database connection 
        self.conn.close() 
 
    def create_treeview(self, date, rows): 
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
        label = ttk.Label(self.tree_frame, text=date, 
font=self.manage_font.large_bold_heading_font) 
        label.pack(pady=5) 
 
        treeview = ttk.Treeview(self.tree_frame, style="Custom.Treeview", 
columns=("ClassName", "Instructor", "Schedule", "Date", "Start Time", "End Time")) 
        treeview.heading("#1", text="Class Name") 
        treeview.heading("#2", text="Instructor") 
        treeview.heading("#3", text="Schedule") 
        treeview.heading("#4", text="Date") 
        treeview.heading("#5", text="Start Time") 
        treeview.heading("#6", text="End Time") 
        treeview.pack(pady=10) 
 
        for row1, row2 in rows: 
            treeview.insert("", "end", values=(row1[0], row1[1], "Schedule 1", 
row1[3], row1[2], self.calculate_end_time(row1[2], row1[4]))) 
            treeview.insert("", "end", values=(row2[0], row2[1], "Schedule 2", 
row2[3], row2[2], self.calculate_end_time(row2[2], row2[4]))) 
 
    def on_frame_configure(self, event): 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
