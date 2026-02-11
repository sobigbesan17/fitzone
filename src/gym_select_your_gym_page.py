import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from gym_font import * 
 
class GymSelectionPage(tk.Tk): 
    def __init__(self, membership_duration_callback): 
        super().__init__() 
         
        self.manage_font = ManageFont() 
         
        self.gym_details_frame = None 
 
        self.frame = tk.Frame(self) 
        self.frame.place(relx=0.5, rely=0.37, anchor=tk.CENTER) 
 
        welcome_label = tk.Label(self.frame, text="Select Your Gym", 
font=self.manage_font.heading_font) 
        welcome_label.pack(pady=20) 
 
        self.conn = sqlite3.connect("FitZone.db") 
        self.cursor = self.conn.cursor() 
 
        select_your_gym_frame = tk.Frame(self.frame, bg="#333333") 
        select_your_gym_frame.pack() 
 
        self.cursor.execute("SELECT LocationName FROM GymLocations") 
        gym_locations = self.cursor.fetchall()
 
        self.location_names = [row[0] for row in gym_locations] 
 
        self.selected_location = tk.StringVar() 
        self.selected_location.set("Select your gym location")   
 
        location_dropdown = ttk.Combobox(select_your_gym_frame, 
textvariable=self.selected_location, values=self.location_names) 
        location_dropdown['state'] = 'readonly'   
        location_dropdown.config(font=self.manage_font.medium_letters_font, 
width=60)   
        location_dropdown.pack(padx=10, pady=10) 
 
        location_dropdown.bind("<<ComboboxSelected>>", self.display_gym_details) 
 
        self.continue_button = tk.Button(select_your_gym_frame, text="Continue", 
width=100, background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font, state="disabled", 
command=self.display_gym_details) 
        self.continue_button.pack(padx=10, pady=10) 
        self.continue_button.bind("<Button-1>", lambda event, 
func=membership_duration_callback: func()) 
 
        self.gym_details_frame = tk.Frame(self.frame, bg="#666666") 
        self.gym_details_frame.pack(pady=20) 
 
    def display_gym_details(self, event=None): 
        selected_gym = self.selected_location.get() 
        self.continue_button["state"] = "normal" 
        if selected_gym != "Select your gym location": 
            self.cursor.execute("SELECT LocationID, Address, EmailAddress, ContactNumber FROM GymLocations WHERE LocationName=?", (selected_gym,)) 
            gym_details = self.cursor.fetchone() 
 
            if self.gym_details_frame: 
                for widget in self.gym_details_frame.winfo_children(): 
                    widget.destroy() 
 
            if gym_details: 
                self.location_id, address, email, contact_number = gym_details 
                gym_info_label = tk.Label(self.gym_details_frame, text=f"Gym Address: {address}\nEmail: {email}\nContact Number: {contact_number}", 
font=self.manage_font.medium_letters_font, width=80, background="#FFE4B5") 
                gym_info_label.pack() 
        else: 
            for widget in self.gym_details_frame.winfo_children(): 
                widget.destroy()
              
    def get_location_id(self): 
        return self.location_id 
