import tkinter as tk 
from tkinter import ttk, messagebox 
import sqlite3 
from tkcalendar import Calendar 
from datetime import datetime, timedelta 
from gym_font import ManageFont 
from gym_function_bank import * 
from PIL import Image, ImageTk 
from tkinter import filedialog 
from gym_workout_recommendation_algorithm import * 
from gym_user_dropdown_menu import * 
 
class GymPersonalisedWorkoutPlanner(tk.Tk): 
    def __init__(self, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback): 
        super().__init__() 
        self.title("Gym Personalised Workout Planner") 
        self.geometry("800x600") 
        self.add_workout_frame = None 
        self.add_workout_title = None 
        self.remove_workout_frame = None 
        self.remove_workout_title = None 
        self.select_workout_frame = None 
        self.select_workout_title = None 
        self.custom_workout_frame = None 
        self.personalised_workout_frame = None 
        self.personalised_workout_title = None 
        self.exercises_title = None 
        self.exercises_frame = None 
        self.workout_recommendation_frame = None 
 
        self.manage_font = ManageFont() 
        self.message_handler = MessageHandler(self) 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, gym_workout_planner_callback, 
view_class_schedule_callback, gym_class_booking_callback, 
gym_class_clashes_callback) 
 
        self.current_date = datetime.datetime.today().date() 
 
        self.conn = sqlite3.connect("FitZone.db") 
        self.cursor = self.conn.cursor() 
         
        self.error_string = "" 
        self.info_string = "" 
        self.success_string = "" 
 
        self.selected_date = self.current_date 
        self.image_path = "" 
 
        self.user_dropdown_menu.pack(fill="x")  
 
        self.canvas = tk.Canvas(self, background="#FFFFFF") 
        self.canvas.pack(fill="both", expand=True) 
 
        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", 
command=self.canvas.yview) 
        self.scrollbar.pack(side="right", fill="y") 
 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.bind("<Configure>", self.configure_canvas) 
 
        self.content_frame = tk.Frame(self.canvas, background="#FFFFFF") 
        self.canvas.create_window((0, 0), window=self.content_frame, 
anchor="nw") 
 
        self.workout_dates = self.get_workout_dates() 
 
        self.add_content() 
 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def configure_canvas(self, event): 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def add_content(self): 
        self.title_label = tk.Label(self.content_frame, text="Personalised Workout Planner", font=self.manage_font.large_bold_heading_font, 
background="#FFFFFF") 
        self.title_label.pack(pady=10) 
 
        self.title_label = tk.Label(self.content_frame, text="Create and manage your custom workouts to achieve your fitness goals.", 
font=self.manage_font.medium_bold_letters_font, background="#FFFFFF") 
        self.title_label.pack(pady=10) 
 
        workout_streak = self.calculate_current_workout_streak() 
 
        highest_workout_streak = self.calculate_highest_workout_streak() 
 
        self.title_label = tk.Label(self.content_frame, text=f"Current Workout Streak: {workout_streak}", font=self.manage_font.medium_bold_heading_font, 
background="#FFFFFF") 
        self.title_label.pack(pady=10) 
 
        self.title_label = tk.Label(self.content_frame, text=f"Maximum Workout Streak: {highest_workout_streak}", 
font=self.manage_font.medium_bold_heading_font, background="#FFFFFF", 
foreground= "#C80000") 
        self.title_label.pack(pady=10) 
 
        self.header_frame = tk.Frame(self.content_frame, background="#CCCCCC") 
        self.header_frame.pack(fill="both") 
 
        self.grid_view = None 
        self.list_view = None 
         
        self.prev_week_button = tk.Button(self.header_frame, text="Previous Week", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.prev_week) 
        self.prev_week_button.pack(side="left", padx=10, pady=10) 
 
        self.next_week_button = tk.Button(self.header_frame, text="Next Week", 
background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.next_week) 
        self.next_week_button.pack(side="right", padx=10, pady=10) 
 
        self.add_workout_button = tk.Button(self.header_frame, text="Add Workout", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_add_workout) 
        self.add_workout_button.pack(side="left", padx=10, pady=10) 
 
        self.remove_workout_button = tk.Button(self.header_frame, text="Remove Workout", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_remove_workout) 
        self.remove_workout_button.pack(side="left", padx=10, pady=10) 
 
        self.select_workout_button = tk.Button(self.header_frame, text="Select Workout", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_select_workout) 
        self.select_workout_button.pack(side="left", padx=10, pady=10) 
 
        self.view_workout_data_button = tk.Button(self.header_frame, text="View Workout Report", background="#FFE4B5", 
font=self.manage_font.medium_bold_letters_font) 
        self.view_workout_data_button.pack(side="left", padx=10, pady=10) 
 
        self.custom_workout_button = tk.Button(self.header_frame, 
text="Personalised Workout Algorithm", background="#FFE4B5", 
font=self.manage_font.medium_bold_letters_font, 
command=self.show_get_personalised_workout) 
        self.custom_workout_button.pack(side="left", padx=10, pady=10) 
 
        self.format_frame = tk.Frame(self.content_frame, background="#FFFFFF")

        self.format_frame.pack(fill="both") 
 
        self.grid_button = tk.Button(self.format_frame, text="Grid Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_grid_view) 
        self.grid_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E) 
 
        self.list_button = tk.Button(self.format_frame, text="List Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_list_view) 
        self.list_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E) 
 
        self.current_date = datetime.datetime.today() 
        self.selected_date = self.current_date.date() 
 
        self.date_picker_frame = tk.LabelFrame(self.content_frame, 
font=self.manage_font.medium_bold_letters_font) 
        self.date_picker_frame.pack(padx=10, pady=10, fill="both", expand=True) 
         
        self.date_picker_label = tk.Label(self.date_picker_frame, text="Select Date:", font=self.manage_font.medium_bold_heading_font) 
        self.date_picker_label.pack(pady=5) 
 
        self.date_picker_calendar = Calendar(self.date_picker_frame, 
selectmode="day", date_pattern="y-mm-dd", 
font=self.manage_font.medium_bold_letters_font, command=self.goto_date) 
        self.date_picker_calendar.pack() 
 
        self.goto_date_button = tk.Button(self.date_picker_frame, text="Go to Date", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.goto_selected_date) 
        self.goto_date_button.pack(pady=5) 
 
        self.workout_schedule_canvas = tk.Canvas(self.content_frame, 
background="#FFFFFF", height=60) 
        self.workout_schedule_canvas.pack(fill="both", expand=True) 
 
        self.show_grid_view() 
 
        self.goto_selected_date() 
 
    def show_add_workout(self): 
        self.destroy_all_frames() 
 
        self.add_workout_title = tk.Frame(self, background="#000000") 
        self.add_workout_title.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        tk.Label(self.add_workout_title, text="Add Workout", font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.add_workout_frame = tk.Frame(self, background="#333333") 
        self.add_workout_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.add_workout_frame, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.add_workout_frame, text="Date (YYYY-MM-DD):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.add_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        time_label = ttk.Label(self.add_workout_frame, text="Time (HH:MM):", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        time_label.pack(padx=10, pady=5) 
        time_entry = ttk.Entry(self.add_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        time_entry.pack(padx=10, pady=5) 
 
        self.cursor.execute(''' 
            SELECT Workouts.WorkoutID, Workouts.WorkoutName, 
SUM(Exercises.Duration) AS TotalExerciseDuration 
            FROM Workouts 
            LEFT JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
            LEFT JOIN Exercises ON WorkoutExercises.ExerciseID = 
Exercises.ExerciseID 
            GROUP BY Workouts.WorkoutID, Workouts.WorkoutName 
        ''') 
 
        self.workout_tuples = self.cursor.fetchall() 
        self.workout_names = [f"{name[1]} ({name[2]} minutes)" for name in 
self.workout_tuples] 
 
        workout_name_label = ttk.Label(self.add_workout_frame, text="Workout Name:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        workout_name_label.pack(padx=10, pady=5) 
        self.workout_name_combobox = ttk.Combobox(self.add_workout_frame, values=self.workout_names, font=self.manage_font.medium_bold_letters_font, 
width=50) 
        self.workout_name_combobox.pack(padx=10, pady=5) 
 
        add_button = tk.Button(self.add_workout_frame, text="Add", 
font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.add_workout(date_entry.get(), time_entry.get(), 
self.get_selected_workout_id())) 
        add_button.pack(padx=10, pady=10) 
 
    def get_selected_workout_id(self): 
        selected_workout = self.workout_name_combobox.get() 
        workout_id = self.workout_tuples[self.workout_names.index(selected_workout)][0] 
        return workout_id 
 
    def show_remove_workout(self): 
        self.destroy_all_frames() 
 
        self.remove_workout_title = tk.Frame(self, background="#000000") 
        self.remove_workout_title.pack(padx=10, pady=0, anchor="center", 
fill="x") 
 
        tk.Label(self.remove_workout_title, text="Remove Workout", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.remove_workout_frame = tk.Frame(self, background="#333333") 
        self.remove_workout_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.remove_workout_frame, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.remove_workout_frame, text="Date (YYYY-MM-DD):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.remove_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        workout_time_label = ttk.Label(self.remove_workout_frame, text="Workout Time (HH:MM):", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 

        workout_time_label.pack(padx=10, pady=5) 
        workout_time_entry = ttk.Entry(self.remove_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        workout_time_entry.pack(padx=10, pady=5) 
 
        remove_button = tk.Button(self.remove_workout_frame, text="Remove Workout", font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.remove_workout_by_time(date_entry.get(), workout_time_entry.get())) 
        remove_button.pack(padx=10, pady=10) 
 
 
    def prev_week(self): 
        self.selected_date -= timedelta(days=7) 
        self.update_workout_schedule() 
 
    def next_week(self): 
        self.selected_date += timedelta(days=7) 
        self.update_workout_schedule() 
 
    def clear_workout_schedule(self): 
        for widget in self.workout_schedule_canvas.winfo_children(): 
            widget.destroy() 
 
    def get_all_exercises(self, workout_name): 
        try: 
            self.cursor.execute(''' 
                SELECT Exercises.ExerciseName, Exercises.ExerciseType, 
Exercises.Description, Exercises.Difficulty, Exercises.TargetedBodyPart, 
Exercises.Duration 
                FROM Workouts 
                LEFT JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
                LEFT JOIN Exercises ON WorkoutExercises.ExerciseID = 
Exercises.ExerciseID 
                WHERE Workouts.WorkoutName = ? 
            ''', (workout_name,)) 
 
            rows = self.cursor.fetchall() 
 
            return rows 
           
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
            return [] 
 
    def get_all_distinct_workout_types(self):
        try: 
            self.cursor.execute("SELECT DISTINCT WorkoutType FROM Workouts") 
 
            workout_types = [row[0] for row in self.cursor.fetchall()] 
 
            return workout_types 
 
        except Exception as e: 
            print("Error while retrieving distinct workout types:", str(e)) 
            return [] 
 
    def get_all_distinct_difficulty_levels(self): 
        try: 
            query = "SELECT DISTINCT Difficulty FROM Workouts" 
            self.cursor.execute(query) 
 
            difficulty_levels = [row[0] for row in self.cursor.fetchall()] 
 
            return difficulty_levels 
 
        except Exception as e: 
            print("Error while retrieving distinct difficulty levels:", str(e)) 
            return [] 
 
    def get_all_distinct_workout_goal_types(self): 
        try: 
            query = "SELECT DISTINCT WorkoutGoal FROM Workouts" 
            self.cursor.execute(query) 
 
            workout_goal_types = [row[0] for row in self.cursor.fetchall()] 
 
            return workout_goal_types 
 
        except Exception as e: 
            print("Error while retrieving distinct workout goal types:", str(e)) 
            return [] 
 
    def calculate_max_workout_count(self, date_range, member_id): 
        max_workouts_per_day = {} 
         
        for date in date_range: 
            self.cursor.execute(''' 
                SELECT COUNT(*) FROM WorkoutSchedules  
                WHERE ScheduledDate = ? AND MemberID = ? 
                ''', (date, member_id)) 
            max_count = self.cursor.fetchone()[0] 
            max_workouts_per_day[date] = max_count 
        return max(max_workouts_per_day.values()) 
 
    def draw_workout_schedule(self): 
        self.clear_workout_schedule() 
 
        workout_schedule_data = self.get_week_workout_schedule(self.selected_date) 
        self.member_id = 1   
 
        self.date_range = [self.selected_date + timedelta(days=i) for i in 
range(7)] 
        self.time_of_day = [""] 
 
        if self.current_view == "grid": 
            self.create_grid_view() 
 
        elif self.current_view == "list": 
            self.create_list_view() 
 
    def create_grid_view(self): 
        max_workout_count = max(self.calculate_max_workout_count(self.date_range, self.member_id), 1) 
 
        self.grid_view = tk.Frame(self.workout_schedule_canvas) 
        self.grid_view.pack(fill="both", expand=True) 
 
        columns = len(self.date_range) 
 
        for index in range(len(self.date_range)): 
            date = self.date_range[index] 
 
            date_frame = tk.Frame(self.grid_view) 
            date_frame.grid(row=0, column=index, padx=10, pady=10, 
sticky="nsew") 
 
            date_label = tk.Label(date_frame, text=f"{date.strftime('%Y-%m-%d')}", background="#333333", foreground="#FFFFFF", width=16, 
font=self.manage_font.medium_bold_heading_font) 
            date_label.grid(row=0, column=0, sticky="nsew") 
 
            self.cursor.execute(''' 
                SELECT UPPER(WorkoutName), ScheduledTime, 
SUM(Exercises.Duration) AS TotalExerciseDuration 
                FROM WorkoutSchedules 
                INNER JOIN Workouts ON WorkoutSchedules.WorkoutID = 
Workouts.WorkoutID 
                INNER JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
                INNER JOIN Exercises ON WorkoutExercises.ExerciseID = 
Exercises.ExerciseID 
                WHERE ScheduledDate = ? AND WorkoutSchedules.MemberID = ? 
                GROUP BY WorkoutName, ScheduledTime 
                ORDER BY ScheduledTime 
            ''', (date, self.member_id)) 
 
            workout_rows = self.cursor.fetchall() 
             
            row_num = 1  
            for row in workout_rows: 
                workout_frame = tk.Frame(date_frame, background="#FFFFFF") 
                workout_frame.grid(row=row_num, column=0, padx=5, pady=5, 
sticky="nsew") 
 
                workout_text = tk.Text(workout_frame, background="#FFFFFF", 
width=15, height=10, font=self.manage_font.medium_bold_letters_font) 
                workout_text.insert("1.0", f"{row[0]}\n({row[1]}) - {row[2]} mins") 
                workout_text.grid(row=0, column=0, sticky="nsew") 
                workout_text.config(state="disabled") 
 
                row_num += 1 
 
            gym_frame = tk.Frame(date_frame, background="#FFFFFF") 
            gym_frame.grid(row=row_num, column=0, padx=5, pady=5, sticky="ew") 
 
    def create_list_view(self): 
        distinct_days = self.get_workout_schedule_days() 
 
        self.title_label = tk.Label(self.workout_schedule_canvas, text=f"From {self.selected_date}", font=self.manage_font.large_bold_heading_font, 
background="white") 
        self.title_label.pack(pady=10) 
 
        if not distinct_days: 
            tk.Label(self.workout_schedule_canvas, text="No workouts recorded for the selected week.", anchor="center", background = "#FFFFFF", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
            tk.Label(self.workout_schedule_canvas, text="Please try another week or", background = "#FFFFFF", 
font=self.manage_font.smaller_letters_font).pack(anchor="center", fill="both", 
padx=10, pady=10) 
 
            message_label = tk.Button(self.workout_schedule_canvas, text="Add workout", font=self.manage_font.medium_bold_letters_font, 
command=self.show_add_workout, background="#333333", foreground="#FFFFFF")

            message_label.pack(anchor="center", padx=10, pady=10) 
 
        for day in distinct_days: 
            list_title_frame = tk.Frame(self.workout_schedule_canvas, 
background="#333333") 
            list_title_frame.pack(padx=0, pady=0) 
                 
            title_label = tk.Label(list_title_frame, text=f"Day: {day}", 
background="#333333", foreground="#FFFFFF", width=160, 
font=self.manage_font.medium_bold_heading_font) 
            title_label.pack(fill="both") 
 
            columns = ["Date", "Start Time", "End Time", "Workouts"] 
            list_view = ttk.Treeview(self.workout_schedule_canvas, 
columns=columns, style="Custom.Treeview", height=4) 
            list_view.pack(fill="both", expand=True) 
 
            list_view["columns"] = columns 
            list_view.heading("#1", text="Date") 
            list_view.heading("#2", text="Start Time") 
            list_view.heading("#3", text="End Time") 
            list_view.heading("#4", text="Workouts") 
 
            workout_names, workout_times, workout_durations = self.get_workout_schedules_for_date(day) 
 
            for i in range(len(workout_names)): 
                workout_name = workout_names[i] 
                workout_start_time = workout_times[i] 
                workout_duration = workout_durations[i] 
                     
                workout_end_time = self.add_minutes_to_time(workout_start_time, 
workout_duration) 
 
                label_text = workout_name 
                label_tag = f"label_{i}" 
                     
                list_view.insert("", "end", values=(day, workout_start_time, 
workout_end_time, workout_name, ""), tags=(label_tag,)) 
 
                list_view.tag_bind(label_tag, "<Button-1>", lambda event, 
name=workout_name, start_time=workout_start_time, 
                                    end_time=workout_end_time: 
self.show_exercises_for_workout(event, name, start_time, end_time)) 
 
 
    def get_workout_dates(self): 
        try:
            self.cursor.execute(''' 
                SELECT ScheduledDate 
                FROM WorkoutSchedules 
                WHERE MemberID = ? AND ScheduledDate < ? 
                ORDER BY ScheduledDate DESC; 
            ''', (1, self.current_date)) 
 
            rows = self.cursor.fetchall() 
            workout_dates = [row[0] for row in rows] 
 
            return workout_dates 
           
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
            return [] 
 
    def calculate_current_workout_streak(self): 
        if not self.workout_dates: 
            return 0 
 
        current_date = self.current_date 
         
        max_streak = 0 
        current_streak = 0 
 
        for date_str in self.workout_dates: 
            workout_date = datetime.datetime.strptime(str(date_str), '%Y-%m-%d').date() 
 
            if (current_date - workout_date).days == 1: 
                current_streak += 1 
                current_date = workout_date 
            else: 
                break 
 
        return current_streak 
 
 
    def calculate_highest_workout_streak(self): 
        if not self.workout_dates: 
            return 0 
 
        current_date = self.current_date 
         
        max_streak = 0 
        current_streak = 0 
        for date_str in self.workout_dates: 
            workout_date = datetime.datetime.strptime(str(date_str), '%Y-%m-%d').date() 
 
            if (current_date - workout_date).days == 1: 
                current_streak += 1 
            else: 
                current_streak = 1 
 
            max_streak = max(max_streak, current_streak) 
            current_date = workout_date 
 
        return max_streak 
 
    def add_minutes_to_time(self, time_str, minutes): 
        time_obj = datetime.datetime.strptime(time_str, "%H:%M") 
        end_time_obj = time_obj + timedelta(minutes=minutes) 
        return end_time_obj.strftime("%H:%M") 
     
    def show_grid_view(self): 
        self.current_view = "grid" 
 
        self.clear_workout_schedule() 
        self.draw_workout_schedule() 
 
        self.workout_schedule_canvas.update_idletasks() 
 
    def show_list_view(self):  
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
        self.current_view = "list" 
        self.clear_workout_schedule() 
        self.create_list_view() 
 
        self.workout_schedule_canvas.update_idletasks() 
 
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
 
    def update_workout_schedule(self): 
        if self.current_view == "grid": 
            self.create_grid_view() 
        elif self.current_view == "list": 
            self.create_list_view() 
 
    def get_workout_schedules_for_date(self, date): 
        try: 
            self.cursor.execute(''' 
                SELECT Workouts.WorkoutName, WorkoutSchedules.ScheduledTime, 
SUM(Exercises.Duration) AS TotalExerciseDuration 
                FROM WorkoutSchedules 
                JOIN Workouts ON WorkoutSchedules.WorkoutID = Workouts.WorkoutID 
                JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
                JOIN Exercises ON WorkoutExercises.ExerciseID = 
Exercises.ExerciseID 
                WHERE WorkoutSchedules.ScheduledDate = ? AND 
WorkoutSchedules.MemberID = ? 
                GROUP BY Workouts.WorkoutName, WorkoutSchedules.ScheduledTime 
                ORDER BY WorkoutSchedules.ScheduledTime 
            ''', (date, 1,)) 
 
            rows = self.cursor.fetchall() 
            workout_names = [row[0] for row in rows] 
            workout_time = [row[1] for row in rows] 
            workout_duration = [row[2] for row in rows] 
            return workout_names, workout_time, workout_duration 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
            return [] 
         
    def get_week_workout_schedule(self, start_date=None): 
        workout_schedule_data = {} 
        if start_date is None: 
            start_date = datetime.datetime.now().date() 
        for i in range(7): 
            current_date = start_date + timedelta(days=i) 
            workouts, _, _ = self.get_workout_schedules_for_date(current_date)

            if workouts: 
                workout_schedule_data[current_date] = {} 
                for workout_entry in workouts: 
                    workout_list = workout_entry[0].split('\n') 
                    current_workout_time = None  
                    for workout in workout_list: 
                        parts = workout.split(":") 
                        if len(parts) == 2: 
                            time, workout_name = parts 
                            current_workout_time = time   
                            workout_schedule_data[current_date].setdefault(current_workout_time, 
[]).append(workout_name.strip()) 
        return workout_schedule_data 
 
    def goto_date(self): 
        selected_date = self.date_picker_calendar.get_date() 
        try: 
            self.selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date() 
            self.update_workout_schedule() 
        except ValueError: 
            self.error_string = f"Error: \n\n \u26A0 Invalid date. Please select a valid date in the format YYYY-MM-DD." 
 
    def goto_selected_date(self): 
        selected_date_str = self.date_picker_calendar.get_date() 
        try: 
            self.selected_date = datetime.datetime.strptime(selected_date_str, 
"%Y-%m-%d").date() 
            self.update_workout_schedule() 
        except ValueError: 
            self.error_string = f"Error: \n\n \u26A0 Invalid date. Please select a valid date in the format YYYY-MM-DD." 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
 
    def calculate_end_time(self, time, workout_duration): 
        hours, minutes = map(int, time.split(":")) 
        start_time = hours * 60 + minutes 
        end_time = start_time + workout_duration 
        return start_time, end_time 
    def check_workout_clashes(self, date, time, workout_id): 
        self.cursor.execute(''' 
            SELECT SUM(Exercises.Duration) AS TotalExerciseDuration 
            FROM Workouts 
            JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
            JOIN Exercises ON WorkoutExercises.ExerciseID = Exercises.ExerciseID 
            WHERE Workouts.WorkoutID = ? 
        ''', (workout_id,)) 
 
        workout_duration = int(self.cursor.fetchone()[0]) 
 
        hours, minutes = divmod(workout_duration, 60) 
        workout_duration_str = f"{hours:02}:{minutes:02}" 
 
        new_start_time, new_end_time = self.calculate_end_time(time, 
workout_duration) 
 
        self.cursor.execute(''' 
            SELECT ScheduledTime, SUM(Exercises.Duration) AS 
TotalExerciseDuration 
            FROM WorkoutSchedules 
            INNER JOIN Workouts ON WorkoutSchedules.WorkoutID = 
Workouts.WorkoutID 
            INNER JOIN WorkoutExercises ON Workouts.WorkoutID = 
WorkoutExercises.WorkoutID 
            INNER JOIN Exercises ON WorkoutExercises.ExerciseID = 
Exercises.ExerciseID 
            WHERE ScheduledDate = ? AND WorkoutSchedules.MemberID = ? 
            GROUP BY ScheduledTime 
        ''', (date, 1,)) 
 
        workout_schedules = self.cursor.fetchall() 
 
        self.overlap_count = 0 
        for scheduled_time, duration in workout_schedules: 
            scheduled_hours, scheduled_minutes = map(int, 
scheduled_time.split(":")) 
            scheduled_start_time = scheduled_hours * 60 + scheduled_minutes 
            scheduled_end_time = scheduled_start_time + duration 
 
            if ((new_start_time >= scheduled_start_time and new_start_time < 
scheduled_end_time) or  
               (new_end_time > scheduled_start_time and new_end_time <= 
scheduled_end_time)):
                self.overlap_count += 1
        return self.overlap_count > 0 
 
    def add_workout(self, date, time, workout_id): 
        try: 
            if workout_id: 
                item = True 
            else: 
                item = False 
 
            self.error_string = "" 
 
            missing_fields = [] 
 
            if not date: 
                missing_fields.append("date") 
            if not time: 
                missing_fields.append("time") 
            if not workout_id: 
                missing_fields.append("workout") 
 
            parsed_time = datetime.datetime.strptime(time, "%H:%M") 
 
            # Formats the time with leading zero 
            formatted_time = parsed_time.strftime("%H:%M") 
 
            clause = ' and ' if len(missing_fields) > 2 else ' and ' 
 
            if missing_fields: 
                if len(missing_fields) == 1: 
                    self.error_string = f"Error: \n\n \u26A0 Please enter {missing_fields[0]}" 
                else: 
                    missing_fields_str = ', '.join(missing_fields[:-1]) + clause + missing_fields[-1] 
                    self.error_string += f"Error: \n\n \u26A0 Please enter {missing_fields_str}" 
 
            if not self.error_string and not self.check_workout_clashes(date, 
formatted_time, workout_id):                       
                if workout_id: 
                    date_str = datetime.datetime.strptime(str(date), '%Y-%m-%d') 
                     
                    if date_str > self.current_date: 
                        self.cursor.execute(''' 
                            INSERT INTO WorkoutSchedules (MemberID, 
ScheduledDate, ScheduledTime, WorkoutID) 
                            VALUES (?, ?, ?, ?) 
                            ''', (1, date, formatted_time, workout_id))

                    else: 
                        self.error_string += f"Error: \n\n \u26A0 You cannot add workouts before today's date." 
            else: 
                if self.check_workout_clashes(date, formatted_time, workout_id): 
                    self.error_string += f"Error: \n\n \u26A0 This workout time clashes with {self.overlap_count} existing workout." 
 
            self.conn.commit() 
            self.update_workout_schedule() 
 
            self.info_string = "Message: \n\n \u2139 Your workout will be added if your input is valid." 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
 
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}") 
 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.info_string: 
                self.message_handler.info_message(self.info_string) 
 
    def remove_workout_by_time(self, workout_date, workout_time): 
        try: 
            self.error_string = "" 
            self.success_string = "" 
             
            if not workout_date and not workout_time: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a valid workout date and time" 
            elif not workout_date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a workout date" 
            elif not workout_time: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a workout time" 
 
            if not self.error_string: 
                    deleted_workout_name = "" 
                     
                    hours, minutes = workout_time.split(":")

                    formatted_workout_time = f"{hours:02}:{minutes:02}" 
 
                    self.cursor.execute('''SELECT WorkoutName FROM Workouts 
                                       WHERE WorkoutID IN ( 
                                           SELECT WorkoutID FROM 
WorkoutSchedules 
                                           WHERE ScheduledDate = ? AND 
ScheduledTime = ? AND MemberID = ? 
                                       )''', (workout_date, 
formatted_workout_time, 1)) 
 
                    deleted_workout_name = self.cursor.fetchone() 
 
                    workout_date_str = datetime.datetime.strptime(str(workout_date), '%Y-%m-%d') 
 
                    if workout_date_str > self.current_date: 
                        self.cursor.execute('''DELETE FROM WorkoutSchedules 
                                            WHERE ScheduledDate = ? AND
                                            ScheduledTime = ? AND MemberID = ? 
                                            ''',(workout_date, 
formatted_workout_time, 1)) 
                    else: 
                        self.error_string = f"Error: \n\n \u26A0 You cannot remove workouts before today's date." 
                        self.message_handler.invalid_message(self.error_string) 
                        return 
                     
                    self.conn.commit() 
                     
                    self.update_workout_schedule() 
                 
                    if deleted_workout_name: 
                        self.success_string = f"Success: \n\n \u2705 Your workout {deleted_workout_name[0]} has been removed!" 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while deleting the workout: {e}") 
            return False 
 
        finally: 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
 
            if not deleted_workout_name: 
                self.error_string = f"Error: \n\n \u26A0 Your workout for{workout_date}, {workout_time} doesn't exist or is an invalid input" 
 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
 
    def view_workout_details(self, date, workout_type): 
        try: 
            workout_details = self.get_workout_schedule_data(date) 
 
            self.error_string = "" 
 
            if not workout_type and not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date and workout type" 
            elif not workout_type: 
                self.error_string = f"Error: \n\n \u26A0 Please enter workout type" 
            elif not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date" 
            elif not workout_details: 
                self.error_string = f"Error: \n\n \u26A0 An error occurred: No {workout_type} found for {date}" 
 
            if not self.error_string: 
                ttk.Separator(self.select_workout_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
                if workout_details: 
                    workout_text = "Workout Details:\n" + "\n".join(workout_details) 
                    workout_label = ttk.Label(self.select_workout_frame, 
text=workout_text, font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
                    workout_label.pack(padx=10, pady=10) 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
 
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}") 
 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
    def update_workout_type_combo(self, workout_type_combo): 
        workout_types = ["Cardio", "Strength Training", "Yoga", "Stretching", 
"Other"] 
        workout_type_combo["values"] = workout_types 
        workout_type_combo.set("") 
 
    def show_select_workout(self): 
        self.destroy_all_frames() 
 
        self.select_workout_title = tk.Frame(self, background="#000000") 
        self.select_workout_title.pack(padx=10, pady=0, anchor="center", 
fill="x") 
 
        tk.Label(self.select_workout_title, text="Select Workout", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.select_workout_frame = tk.Frame(self, background="#333333") 
        self.select_workout_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.select_workout_frame, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.select_workout_frame, text="Date (YYYY-MM-DD):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.select_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        workout_time_label = ttk.Label(self.select_workout_frame, text="Workout Time:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        workout_time_label.pack(padx=10, pady=5) 
        workout_time_entry = ttk.Entry(self.select_workout_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        workout_time_entry.pack(padx=10, pady=5) 
 
        view_details_button = tk.Button(self.select_workout_frame, text="View Details", font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.view_workout_details(date_entry.get(), workout_time_entry.get())) 
        view_details_button.pack(padx=10, pady=10) 
 
    def show_exercises_for_workout(self, event, workout_name, workout_start_time, workout_end_time): 
        self.destroy_all_frames() 
 
        self.exercises_title = tk.Frame(self, background="#000000") 
        self.exercises_title.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        tk.Label(self.exercises_title, text=f"Exercises for Workout: {workout_name} ({workout_start_time}-{workout_end_time})", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.exercises_frame = tk.Frame(self, background="#333333") 
        self.exercises_frame.pack(padx=10, pady=0, anchor="center", fill="both") 
 
        canvas = tk.Canvas(self.exercises_frame, background="#FFFFFF")   
        canvas.pack(side="left", fill="both", expand=True) 
 
        scrollbar = tk.Scrollbar(self.exercises_frame, orient="vertical", 
command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") 
 
        canvas.configure(yscrollcommand=scrollbar.set) 
 
        exercise_container = tk.Frame(canvas, background="#FFFFFF") 
        canvas.create_window((0, 0), window=exercise_container, anchor="nw") 
 
        close_button = tk.Button(exercise_container, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.pack(padx=10, pady=10, anchor='ne') 
 
        exercises = self.get_all_exercises(workout_name) 
 
        tk.Label(exercise_container, text=f"Workout Exercises", 
font=self.manage_font.medium_bold_heading_font, background="#333333", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        if exercises: 
            exercise_table = ttk.Treeview(exercise_container, columns=("Exercise Name", "Type", "Description", "Difficulty", "Targeted Body Part", "Duration (Minutes)"), style="Custom.Treeview", show="headings", height=15) 
            exercise_table.heading("Exercise Name", text="Exercise Name") 
            exercise_table.heading("Type", text="Type") 
            exercise_table.heading("Description", text="Description") 
            exercise_table.heading("Difficulty", text="Difficulty") 
            exercise_table.heading("Targeted Body Part", text="Targeted Body Part") 
            exercise_table.heading("Duration (Minutes)", text="Duration (Minutes)") 
 
            for exercise in exercises: 
                exercise_table.insert("", "end", values=exercise) 
 
            exercise_table.pack(padx=10, pady=10) 
 
            exercise_start_time = workout_start_time 
 
            # Create a frame for each exercise to display additional details 
            for exercise in exercises: 
                exercise_time_frame = tk.Frame(exercise_container, 
background="#333333")   
                exercise_time_frame.pack(padx=10, pady=10, anchor="center", 
fill="both") 
 
                exercise_end_time = self.add_minutes_to_time(exercise_start_time, exercise[5]) 
                 
                tk.Label(exercise_time_frame, text=f"Time: {exercise_start_time} - {exercise_end_time}", font=self.manage_font.medium_bold_heading_font, 
background="#333333", foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
                 
                exercise_frame = tk.Frame(exercise_container, 
background="#FFFFFF")  # Set background color to white 
                exercise_frame.pack(padx=10, pady=10, anchor="center", 
fill="both") 
 
                tk.Label(exercise_frame, text=f"Exercise: {exercise[0]}", 
font=self.manage_font.medium_bold_heading_font).pack(padx=10, pady=0, fill="x") 
                tk.Label(exercise_frame, text=f"Type: {exercise[1]}", 
font=self.manage_font.medium_letters_font).pack(padx=10, pady=0, fill="x") 
                tk.Label(exercise_frame, text=f"Description: {exercise[2]}", 
font=self.manage_font.medium_letters_font).pack(padx=10, pady=0, fill="x") 
                tk.Label(exercise_frame, text=f"Difficulty: {exercise[3]}", 
font=self.manage_font.medium_letters_font).pack(padx=10, pady=0, fill="x") 
                tk.Label(exercise_frame, text=f"Targeted Body Part: {exercise[4]}", font=self.manage_font.medium_letters_font).pack(padx=10, pady=0, 
fill="x") 
                tk.Label(exercise_frame, text=f"Duration: {exercise[5]} minutes", font=self.manage_font.medium_letters_font).pack(padx=10, pady=0, 
fill="x") 
 
                exercise_start_time = str(exercise_end_time) 
 
                more_info_button = tk.Button(exercise_frame, text="More Info", 
background="#FFE4B5", font=self.manage_font.medium_bold_heading_font, 
command=lambda exercise=exercise: self.show_more_info(exercise)) 

                more_info_button.pack(padx=10, pady=10, fill="x") 
        else: 
            tk.Label(exercise_container, text="No exercises found for this workout.", font=self.manage_font.medium_letters_font).pack(padx=10, pady=10) 
 
        exercise_container.update_idletasks() 
        canvas.config(scrollregion=canvas.bbox("all")) 
 
    def show_remove_custom_workout(self): 
        self.destroy_all_frames() 
 
        self.remove_workout_title = tk.Frame(self, background="#000000") 
        self.remove_workout_title.pack(padx=10, pady=0, anchor="center", 
fill="x") 
 
        tk.Label(self.remove_workout_title, text="Remove Custom Workout", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.remove_workout_frame = tk.Frame(self, background="#333333") 
        self.remove_workout_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.remove_workout_frame, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        custom_workout_name_label = ttk.Label(self.remove_workout_frame, 
text="Custom Workout Name:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        custom_workout_name_label.pack(padx=10, pady=5) 
        custom_workout_name_combo = ttk.Combobox(self.remove_workout_frame, 
values=self.select_all_custom_workout(), 
font=self.manage_font.medium_bold_letters_font, width=50) 
        custom_workout_name_combo.pack(padx=10, pady=5) 
 
        remove_button = tk.Button(self.remove_workout_frame, text="Remove", 
font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.remove_custom_workout_by_name(custom_workout_name_combo.get())) 
        remove_button.pack(padx=10, pady=10) 
 
    def show_get_personalised_workout(self): 
        self.destroy_all_frames() 
 
        self.personalised_workout_title = tk.Frame(self, background="#000000") 
        self.personalised_workout_title.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        tk.Label(self.personalised_workout_title, text="Get Personalised Workout", font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.personalised_workout_frame = tk.Frame(self, background="#333333") 
        self.personalised_workout_frame.pack(padx=10, pady=0, anchor="center", fill="both") 
 
        canvas = tk.Canvas(self.personalised_workout_frame, width=600, 
height=300, background="#333333") 
        canvas.pack(side="left", fill="both", expand=True) 
 
        scrollbar = ttk.Scrollbar(self.personalised_workout_frame, 
orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") 
 
        canvas.configure(yscrollcommand=scrollbar.set) 
 
        self.frame_in_canvas = tk.Frame(canvas, background="#333333") 
 
        canvas.create_window((0, 0), window=self.frame_in_canvas, anchor="nw") 
 
        close_button = tk.Button(self.frame_in_canvas, text="\u2716", 
fg="#FFFFFF", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.grid(row=0, column=4, sticky="ne") 
 
        row_num = 1 
        label_entries = [ 
            ("Equipment:", "equipment_entry"), 
            ("Target BMI:", "target_bmi_entry"), 
        ] 
 
        for label_text, entry_name in label_entries: 
            label = ttk.Label(self.frame_in_canvas, text=label_text, 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
            label.grid(row=row_num, column=0, padx=10, pady=5, sticky="w") 
 
            entry = ttk.Entry(self.frame_in_canvas, 
font=self.manage_font.medium_bold_letters_font, width=50) 
            setattr(self, entry_name, entry) 
 
            if label_text == "Target BMI:" or label_text == "Calories Burn Target:": 
                validate_entry = self.register(self.check_numeric_input)
                entry.config(validate="key", validatecommand=(validate_entry, "%P", 3)) 
                 
            entry.grid(row=row_num, column=1, padx=10, pady=5) 
            row_num += 1 
 
        difficulty_levels = self.get_all_distinct_difficulty_levels() 
 
        selected_difficulty = tk.StringVar(value=difficulty_levels[0]) 
        self.difficulty_combobox = ttk.Combobox(self.frame_in_canvas, 
textvariable=selected_difficulty, 
font=self.manage_font.medium_bold_letters_font, values=difficulty_levels, 
width=50) 
        self.difficulty_combobox.grid(row=3, column=1, padx=10, pady=5, 
sticky="w") 
 
        difficulty_label = ttk.Label(self.frame_in_canvas, text="Difficulty Level:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        difficulty_label.grid(row=3, column=0, padx=10, pady=5, sticky="w") 
 
        workout_types_label = ttk.Label(self.frame_in_canvas, text="Workout Type:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        workout_types_label.grid(row=1, column=2, padx=10, pady=5, sticky="w") 
 
        workout_types = self.get_all_distinct_workout_types() 
        selected_type = tk.StringVar(value=workout_types[0]) 
 
        self.workout_types_combobox = ttk.Combobox(self.frame_in_canvas, 
textvariable=selected_type, font=self.manage_font.medium_bold_letters_font, 
values=workout_types, width=50) 
        self.workout_types_combobox.grid(row=1, column=3, padx=10, pady=5, 
sticky="w") 
 
        workout_goals_label = ttk.Label(self.frame_in_canvas, text="Workout Goal:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        workout_goals_label.grid(row=2, column=2, padx=10, pady=5, sticky="w") 
 
        workout_goals = self.get_all_distinct_workout_goal_types() 
        selected_goal = tk.StringVar(value=workout_goals[0]) 
 
        self.workout_goals_combobox = ttk.Combobox(self.frame_in_canvas, 
textvariable=selected_goal, font=self.manage_font.medium_bold_letters_font, 
values=workout_goals, width=50) 
        self.workout_goals_combobox.grid(row=2, column=3, padx=10, pady=5, 
sticky="w")
 
        get_workout_button = tk.Button(self.frame_in_canvas, text="Get Recommended Workout", font=self.manage_font.medium_bold_heading_font, 
background="#00BFFF", foreground="#FFFFFF", width=70, command=lambda: 
self.get_workout_recommendation()) 
        get_workout_button.grid(row=row_num+2, column=3, columnspan=2, 
rowspan=2, padx=10, pady=10) 
 
        self.frame_in_canvas.bind("<Configure>", lambda event, canvas=canvas: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def get_workout_recommendation(self): 
        user_input = { 
            "Equipment": self.equipment_entry.get(), 
            "DifficultyLevel": self.difficulty_combobox.get(), 
            "TargetBMI": self.target_bmi_entry.get(), 
            "WorkoutType": self.workout_types_combobox.get(), 
            "WorkoutGoal": self.workout_goals_combobox.get(), 
        } 
 
        # Recommendation algorithm for workouts with exercises 
        recommendation_algorithm = GymWorkoutRecommendationAlgorithm() 
        recommendation_algorithm.load_data() 
        recommendation_algorithm.preprocess_data() 
        recommended_workout_details = recommendation_algorithm.get_recommendation(user_input) 
 
        if self.workout_recommendation_frame: 
            self.workout_recommendation_frame.destroy() 
 
        self.workout_recommendation_frame = tk.Frame(self.frame_in_canvas, 
background="#FFFFFF") 
        self.workout_recommendation_frame.grid(row=19, column=0, columnspan=2, 
padx=10, pady=5, sticky="w") 
 
        close_button = tk.Button(self.workout_recommendation_frame, 
text="\u2716", background="#D11A17", foreground="#FFFFFF", command=lambda 
frame=self.workout_recommendation_frame: frame.destroy()) 
        close_button.grid(row=0, column=2, sticky=tk.NE) 
 
        workout_details_label = ttk.Label(self.workout_recommendation_frame, 
text="Recommended Workout:", font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF") 
        workout_details_label.grid(row=1, column=0, padx=10, pady=5, sticky="w") 
 
        workout_details_label = ttk.Label(self.workout_recommendation_frame, 
text=recommended_workout_details, 
font=self.manage_font.medium_bold_letters_font, background="#FFFFFF") 

        workout_details_label.grid(row=2, column=0, columnspan=2, padx=10, 
pady=5, sticky="w") 
 
    def get_workout_schedule_days(self): 
        try: 
            current_date = datetime.datetime.now().strftime("%Y-%m-%d") 
 
            self.cursor.execute(''' 
                SELECT DISTINCT ScheduledDate 
                FROM WorkoutSchedules 
                WHERE ScheduledDate >= ? AND MemberID = ? 
                ORDER BY ScheduledDate, ScheduledTime 
            ''', (self.selected_date, self.member_id)) 
            rows = self.cursor.fetchall() 
            workout_days = [row[0] for row in rows] 
            return workout_days 
         
        except sqlite3.Error as e: 
            print("An error occurred with the database:", e) 
            return [] 
 
    def select_workouts_by_type(self, data): 
        try: 
            self.cursor.execute(''' 
                SELECT WorkoutName FROM CustomWorkouts 
                WHERE WorkoutType = ? AND MemberID = ? 
            ''', (data, 1)) 
            custom_workout_rows = self.cursor.fetchall() 
            custom_workout_names = [row[0] for row in custom_workout_rows] 
            return custom_workout_names 
        except sqlite3.Error as e: 
            print("An error occurred with the database:", e) 
            return [] 
 
    def destroy_all_frames(self): 
        if self.add_workout_frame: 
            self.add_workout_frame.destroy() 
        if self.add_workout_title: 
            self.add_workout_title.destroy() 
 
        if self.remove_workout_frame: 
            self.remove_workout_frame.destroy() 
        if self.remove_workout_title: 
            self.remove_workout_title.destroy() 
 
        if self.select_workout_frame: 
            self.select_workout_frame.destroy() 
        if self.select_workout_title:
            self.select_workout_title.destroy() 
 
        if self.custom_workout_frame: 
            self.custom_workout_frame.destroy() 
 
        if self.personalised_workout_frame: 
            self.personalised_workout_frame.destroy() 
        if self.personalised_workout_title: 
            self.personalised_workout_title.destroy() 
 
        if self.exercises_title: 
            self.exercises_title.destroy() 
        if self.exercises_frame: 
            self.exercises_frame.destroy() 
 
    def check_numeric_input(self, string, length): 
        return (string.isdigit() or string == "") and len(string) <= int(length) 
 
    def update_workout_schedule(self): 
        self.draw_workout_schedule() 
         
if __name__ == "__main__": 
    app = GymPersonalisedWorkoutPlanner(1, None, None, None, None, None, None, 
None, None).mainloop() 
