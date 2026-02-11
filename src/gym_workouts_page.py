import tkinter as tk
from tkinter import ttk
from gym_font import ManageFont
import sqlite3

class GymWorkoutPage(tk.Toplevel):
    def __init__(self, parent, member_id=None):
        super().__init__(parent)
        self.title("Gym Workout Plans")
        self.geometry("700x500")
        self.configure(bg="#f2f2f2")

        self.member_id = member_id
        self.manage_font = ManageFont()

        heading_label = tk.Label(self, text="Select Your Gym Workout Plan",
                                 font=self.manage_font.heading_font,
                                 bg="#f2f2f2", fg="#333333")
        heading_label.pack(pady=(20, 10))

        instruction_label = tk.Label(self, text="Choose a workout plan tailored to your fitness goals:",
                                     font=self.manage_font.medium_letters_font,
                                     bg="#f2f2f2", fg="#333333")
        instruction_label.pack(pady=(5, 10))

        self.workout_var = tk.StringVar()
        workout_options = ["Strength Training", "Cardio Endurance", "Flexibility & Mobility", "HIIT Program"]
        workout_menu = ttk.Combobox(self, textvariable=self.workout_var,
                                    values=workout_options, state="readonly",
                                    font=self.manage_font.medium_letters_font, width=40)
        workout_menu.pack(pady=10)
        workout_menu.current(0)

        confirm_button = tk.Button(self, text="Confirm Workout Plan",
                                   font=self.manage_font.medium_bold_heading_font,
                                   bg="#C62E46", fg="white", width=25,
                                   command=self.save_workout_plan)
        confirm_button.pack(pady=(20, 10))

        self.status_label = tk.Label(self, text="", bg="#f2f2f2",
                                     font=self.manage_font.smaller_letters_font,
                                     fg="green")
        self.status_label.pack(pady=10)

        self.display_workout_info()

    def display_workout_info(self):
        info_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.GROOVE)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(info_frame, text="Workout Plan Information",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#ffffff", fg="#333333").pack(pady=(10, 5))

        self.workout_info_text = tk.Text(info_frame, wrap="word",
                                         font=self.manage_font.medium_letters_font,
                                         bg="#ffffff", fg="#333333", height=10, width=70)
        self.workout_info_text.pack(padx=10, pady=10)
        self.workout_info_text.insert("1.0", "Select a workout plan to view details here.")
        self.workout_info_text.config(state="disabled")

    def save_workout_plan(self):
        workout_plan = self.workout_var.get()
        try:
            conn = sqlite3.connect("FitZone.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Members
                SET WorkoutPlan = ?
                WHERE MemberID = ?
            """, (workout_plan, self.member_id))
            conn.commit()
            conn.close()
            self.status_label.config(text=f"Workout plan '{workout_plan}' saved successfully!", fg="green")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error saving workout plan: {e}", fg="red")
