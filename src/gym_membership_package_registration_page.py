import tkinter as tk
from tkinter import ttk
from gym_font import ManageFont
import sqlite3

class GymMembershipPackageRegistrationPage(tk.Toplevel):
    def __init__(self, parent, member_id=None):
        super().__init__(parent)
        self.title("Membership Package Registration")
        self.geometry("600x400")
        self.configure(bg="#f2f2f2")

        self.member_id = member_id
        self.manage_font = ManageFont()

        # Heading
        heading_label = tk.Label(self, text="Register Membership Package",
                                 font=self.manage_font.heading_font,
                                 bg="#f2f2f2", fg="#333333")
        heading_label.pack(pady=(20, 10))

        # Instruction
        instruction_label = tk.Label(self, text="Select your membership package:",
                                     font=self.manage_font.medium_letters_font,
                                     bg="#f2f2f2", fg="#333333")
        instruction_label.pack(pady=(5, 10))

        # Dropdown for package selection
        self.package_var = tk.StringVar()
        package_options = ["Basic", "Standard", "Premium", "Elite"]
        package_menu = ttk.Combobox(self, textvariable=self.package_var,
                                    values=package_options, state="readonly",
                                    font=self.manage_font.medium_letters_font)
        package_menu.pack(pady=10)
        package_menu.current(0)

        # Confirmation button
        confirm_button = tk.Button(self, text="Confirm Package",
                                   font=self.manage_font.medium_bold_heading_font,
                                   bg="#C62E46", fg="white", width=20,
                                   command=self.save_membership_package)
        confirm_button.pack(pady=(20, 10))

        # Status message
        self.status_label = tk.Label(self, text="", bg="#f2f2f2",
                                     font=self.manage_font.smaller_letters_font,
                                     fg="green")
        self.status_label.pack(pady=10)

    def save_membership_package(self):
        package = self.package_var.get()

        try:
            conn = sqlite3.connect("FitZone.db")
            cursor = conn.cursor()

            # Example: store package in Memberships table
            cursor.execute("""
                UPDATE Memberships
                SET Package = ?
                WHERE MemberID = ?
            """, (package, self.member_id))

            conn.commit()
            conn.close()

            self.status_label.config(text=f"Membership package '{package}' saved successfully!")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error saving package: {e}", fg="red")
