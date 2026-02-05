import tkinter as tk 
from tkinter import ttk 
from gym_font import ManageFont 
from gym_function_bank import * 
import sqlite3 
 
class GymRegistrationSuccessPage(tk.Tk): 
    def __init__(self, users_detail, home_callback): 
        super().__init__() 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
         
        self.title("Registration Success") 
        self.geometry("800x600") 
        self.home_callback = home_callback 
        self.users_detail = users_detail 
 
        self.manage_font = ManageFont() 
        self.users_detail = users_detail 
 
        self.add_new_member() 
         
        self.create_registration_success_page() 
 
    def create_registration_success_page(self): 
        registration_success_frame = ttk.Frame(self, style='TFrame') 
        registration_success_frame.pack(fill='both', expand=True, pady=160) 
 
        success_label = ttk.Label(registration_success_frame, text="Registration Successful!", font=self.manage_font.large_bold_heading_font) 
        success_label.pack(pady=50) 
 
        success_message = ttk.Label(registration_success_frame, text="Thank you 
for registering at FitZone. Your membership has been successfully created.", 
font=self.manage_font.medium_letters_font) 
        success_message.pack(pady=20) 
 
        self.back_button = tk.Button(registration_success_frame, 
text="Continue", width=100, background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font) 
        self.back_button.pack(padx=10, pady=10) 
        self.back_button.bind("<Button-1>", lambda event, func=self.home_callback: func())

    def add_new_member(self): 
        try: 
            insert_query = ''' 
                INSERT INTO Members (LocationID, DurationID, PackageID, 
Username, Password, Salt, Gender, Email, DateOfBirth, JoinDate, FirstName, 
LastName, \ 
                Address, CountryCode, PhoneNumber, ImagePath, 
EmailNotifications) \ 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            ''' 
 
            member_data = (self.users_detail[0], self.users_detail[1], 
self.users_detail[2], self.users_detail[3], self.users_detail[4], 
self.users_detail[5], self.users_detail[6] 
                           , self.users_detail[7], self.users_detail[8], 
self.users_detail[9], self.users_detail[10], self.users_detail[11], 
self.users_detail[12], self.users_detail[13] 
                           , self.users_detail[14], self.users_detail[15], 
self.users_detail[16]) 
             
            self.cursor.execute(insert_query, member_data) 
            self.conn.commit() 
            return True 
        except sqlite3.Error as e: 
            print("Error inserting member:", e) 
            return False
