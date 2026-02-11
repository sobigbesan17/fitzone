import tkinter as tk
from tkinter import ttk
from gym_font import ManageFont
import sqlite3

class GymMealPage(tk.Toplevel):
    def __init__(self, parent, member_id=None):
        super().__init__(parent)
        self.title("Gym Meal Plans")
        self.geometry("700x500")
        self.configure(bg="#f2f2f2")

        self.member_id = member_id
        self.manage_font = ManageFont()

        heading_label = tk.Label(self, text="Select Your Gym Meal Plan",
                                 font=self.manage_font.heading_font,
                                 bg="#f2f2f2", fg="#333333")
        heading_label.pack(pady=(20, 10))

        instruction_label = tk.Label(self, text="Choose a meal plan tailored to your fitness goals:",
                                     font=self.manage_font.medium_letters_font,
                                     bg="#f2f2f2", fg="#333333")
        instruction_label.pack(pady=(5, 10))

        self.meal_var = tk.StringVar()
        meal_options = ["Weight Loss Plan", "Muscle Gain Plan", "Balanced Nutrition Plan", "Vegan Plan"]
        meal_menu = ttk.Combobox(self, textvariable=self.meal_var,
                                 values=meal_options, state="readonly",
                                 font=self.manage_font.medium_letters_font, width=40)
        meal_menu.pack(pady=10)
        meal_menu.current(0)

        confirm_button = tk.Button(self, text="Confirm Meal Plan",
                                   font=self.manage_font.medium_bold_heading_font,
                                   bg="#C62E46", fg="white", width=25,
                                   command=self.save_meal_plan)
        confirm_button.pack(pady=(20, 10))

        self.status_label = tk.Label(self, text="", bg="#f2f2f2",
                                     font=self.manage_font.smaller_letters_font,
                                     fg="green")
        self.status_label.pack(pady=10)

        self.display_meal_info()

    def display_meal_info(self):
        info_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.GROOVE)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(info_frame, text="Meal Plan Information",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#ffffff", fg="#333333").pack(pady=(10, 5))

        self.meal_info_text = tk.Text(info_frame, wrap="word",
                                      font=self.manage_font.medium_letters_font,
                                      bg="#ffffff", fg="#333333", height=10, width=70)
        self.meal_info_text.pack(padx=10, pady=10)
        self.meal_info_text.insert("1.0", "Select a meal plan to view details here.")
        self.meal_info_text.config(state="disabled")

    def save_meal_plan(self):
        meal_plan = self.meal_var.get()
        try:
            conn = sqlite3.connect("FitZone.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Members
                SET MealPlan = ?
                WHERE MemberID = ?
            """, (meal_plan, self.member_id))
            conn.commit()
            conn.close()
            self.status_label.config(text=f"Meal plan '{meal_plan}' saved successfully!", fg="green")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error saving meal plan: {e}", fg="red")
