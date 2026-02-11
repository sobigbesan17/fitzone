import tkinter as tk
from tkinter import ttk, messagebox
from gym_font import ManageFont
from gym_header import *
from gym_footer import GymFooter
import sqlite3

class GymFeaturesRegistrationPage(tk.Tk):
    def __init__(self, home_callback):
        super().__init__()
        self.home_callback = home_callback
        self.manage_font = ManageFont()
        self.conn = sqlite3.connect("FitZone.db")
        self.cursor = self.conn.cursor()
        self.title("Gym Features Registration")
        self.geometry("900x700")
        self.canvas = tk.Canvas(self, bg="#FFFFFF")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.update_scroll)
        self.main_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.create_header()
        self.create_form()
        self.create_footer()

    def update_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_header(self):
        header = GymHeader(self.main_frame, self.home_callback)
        header.pack(fill="x")

    def create_form(self):
        form_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        form_frame.pack(pady=20, padx=20, fill="both")

        tk.Label(form_frame, text="Register Your Gym Preferences", 
                 font=self.manage_font.large_bold_heading_font, bg="#FFFFFF").pack(pady=10)

        tk.Label(form_frame, text="Fitness Goal", 
                 font=self.manage_font.medium_bold_letters_font, bg="#FFFFFF").pack()
        self.goal_entry = ttk.Entry(form_frame, width=60)
        self.goal_entry.pack(pady=5)

        tk.Label(form_frame, text="Experience Level (1–10)", 
                 font=self.manage_font.medium_bold_letters_font, bg="#FFFFFF").pack()
        self.experience_entry = ttk.Entry(form_frame, width=60)
        self.experience_entry.pack(pady=5)

        tk.Label(form_frame, text="Preferred Workout Type", 
                 font=self.manage_font.medium_bold_letters_font, bg="#FFFFFF").pack()
        self.workout_type_entry = ttk.Entry(form_frame, width=60)
        self.workout_type_entry.pack(pady=5)

        tk.Label(form_frame, text="Available Equipment (comma-separated)", 
                 font=self.manage_font.medium_bold_letters_font, bg="#FFFFFF").pack()
        self.equipment_entry = ttk.Entry(form_frame, width=60)
        self.equipment_entry.pack(pady=5)

        tk.Label(form_frame, text="Target Muscles (comma-separated)", 
                 font=self.manage_font.medium_bold_letters_font, bg="#FFFFFF").pack()
        self.muscles_entry = ttk.Entry(form_frame, width=60)
        self.muscles_entry.pack(pady=5)

        tk.Button(form_frame, text="Save Preferences", 
                  font=self.manage_font.medium_bold_heading_font,
                  bg="#C62E46", fg="#FFFFFF", width=40,
                  command=self.save_preferences).pack(pady=20)

    def save_preferences(self):
        goal = self.goal_entry.get()
        experience = self.experience_entry.get()
        workout_type = self.workout_type_entry.get()
        equipment = self.equipment_entry.get()
        muscles = self.muscles_entry.get()

        if not goal or not experience or not workout_type:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO UserFeatures (FitnessGoal, ExperienceLevel, WorkoutType, Equipment, TargetMuscles)
                VALUES (?, ?, ?, ?, ?)
            """, (goal, experience, workout_type, equipment, muscles))
            self.conn.commit()
            messagebox.showinfo("Success", "Preferences saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_footer(self):
        footer = GymFooter(self.main_frame)
        footer.pack(fill="x")
