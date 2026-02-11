import tkinter as tk
from tkinter import ttk
from gym_font import ManageFont
from gym_login import GymLogin  

class GymFooter(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#333333")
        self.parent = parent
        self.manage_font = ManageFont()

        # Separator line
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", pady=5)

        footer_frame = tk.Frame(self, bg="#333333")
        footer_frame.pack(fill="x", padx=20, pady=10)

        help_frame = tk.Frame(footer_frame, bg="#333333")
        help_frame.grid(row=0, column=0, padx=20, sticky="nw")
        tk.Label(help_frame, text="Help & Contact",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(help_frame, text="Email: support@fitzone.com",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(help_frame, text="Phone: +44 1234 567890",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")

        social_frame = tk.Frame(footer_frame, bg="#333333")
        social_frame.grid(row=0, column=1, padx=20, sticky="nw")
        tk.Label(social_frame, text="Follow Us",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(social_frame, text="Instagram: @fitzone",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(social_frame, text="Twitter: @fitzone",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(social_frame, text="Facebook: FitZone Gym",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")

        services_frame = tk.Frame(footer_frame, bg="#333333")
        services_frame.grid(row=0, column=2, padx=20, sticky="nw")
        tk.Label(services_frame, text="Gym Services",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(services_frame, text="Fitness Classes",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(services_frame, text="Personal Instructors",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")
        tk.Label(services_frame, text="Nutrition Guidance",
                 font=self.manage_font.smaller_letters_font,
                 bg="#333333", fg="white").pack(anchor="w")

        login_frame = tk.Frame(footer_frame, bg="#333333")
        login_frame.grid(row=0, column=3, padx=20, sticky="nw")
        tk.Label(login_frame, text="Member Access",
                 font=self.manage_font.medium_bold_heading_font,
                 bg="#333333", fg="white").pack(anchor="w")
        login_button = tk.Button(login_frame, text="Login",
                                 font=self.manage_font.medium_bold_letters_font,
                                 bg="#C62E46", fg="white", width=15,
                                 command=self.open_login)
        login_button.pack(anchor="w", pady=5)

    def open_login(self):
        GymLogin(self.parent)
