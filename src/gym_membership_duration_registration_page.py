import tkinter as tk
from tkinter import ttk
from gym_font import ManageFont
import sqlite3

class GymMembershipDurationRegistrationPage(tk.Toplevel):
    def __init__(self, parent, member_id=None):
        super().__init__(parent)
        self.title("Membership Duration Registration")
        self.geometry("600x400")
        self.configure(bg="#f2f2f2")

        self.member_id = member_id
        self.manage_font = ManageFont()

        # Heading
        heading_label = tk.Label(self, text="Register Membership Duration",
                                 font=self.manage_font.heading_font,
                                 bg="#f2f2f2", fg="#333333")
        heading_label.pack(pady=(20, 10))

        # Instruction
        instruction_label = tk.Label(self, text="Select your membership duration:",
                                     font=self.manage_font.medium_letters_font,
                                     bg="#f2f2f2", fg="#333333")
        instruction_label.pack(pady=(5, 10))

        # Dropdown for duration
        self.duration_var = tk.StringVar()
        duration_options = ["1 Month", "3 Months", "6 Months", "12 Months"]
        duration_menu = ttk.Combobox(self, textvariable=self.duration_var,
                                     values=duration_options, state="readonly",
                                     font=self.manage_font.medium_letters_font)
        duration_menu.pack(pady=10)
        duration_menu.current(0)

        # Confirmation button
        confirm_button = tk.Button(self, text="Confirm Duration",
                                   font=self.manage_font.medium_bold_heading_font,
                                   bg="#C62E46", fg="white", width=20,
                                   command=self.save_membership_duration)
        confirm_button.pack(pady=(20, 10))

        # Status message
        self.status_label = tk.Label(self, text="", bg="#f2f2f2",
                                     font=self.manage_font.smaller_letters_font,
                                     fg="green")
        self.status_label.pack(pady=10)

    def save_membership_duration(self):
        duration = self.duration_var.get()

        try:
            conn = sqlite3.connect("FitZone.db")
            cursor = conn.cursor()

            # Example: store duration in Memberships table
            cursor.execute("""
                UPDATE Memberships
                SET Duration = ?
                WHERE MemberID = ?
            """, (duration, self.member_id))

            conn.commit()
            conn.close()

            self.status_label.config(text=f"Membership duration '{duration}' saved successfully!")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error saving duration: {e}", fg="red")
