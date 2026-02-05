import sqlite3 
import tkinter as tk 
from tkinter import ttk 
from gym_font import ManageFont 
from gym_function_bank import * 
 
class GymSetNewPassword(tk.Tk): 
    def __init__(self, member_id, login_callback): 
        super().__init__() 
         
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.member_id = member_id 
 
        self.functions_back = ManageFont() 
         
        self.message_handler = MessageHandler(self) 
         
        self.validate_credentials = ValidateCredentials() 
 
        set_password_frame = tk.Frame(self, background="#333333") 
        set_password_frame.place(relx=0.5, rely=0.385, anchor=tk.CENTER, 
width=940) 
 
        self.set_password_frame = set_password_frame 
 
        self.manage_font = ManageFont() 
 
        self.password_entry = ttk.Entry(set_password_frame, width=60, show='*', 
font=self.manage_font.medium_bold_letters_font) 
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew", 
columnspan=6) 
        self.confirm_password_entry = ttk.Entry(set_password_frame, width=60, 
show='*', font=self.manage_font.medium_bold_letters_font) 
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5, 
sticky="ew", columnspan=6) 
 
        self.password_entry.bind("<KeyRelease>", self.clear_success_message) 
        self.confirm_password_entry.bind("<KeyRelease>", 
self.clear_success_message) 
 
        style = ttk.Style(self) 
        style.configure("TFrame", background="#333333", foreground="#FFFFFF") 
 
        description_label = tk.Label(set_password_frame, text="Set New Password", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.large_bold_heading_font)
        description_label.grid(row=0, column=0, padx=10, pady=5, columnspan=7, 
sticky="w") 
 
        password_label = tk.Label(set_password_frame, text="New Password:", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w") 
 
        confirm_password_label = tk.Label(set_password_frame, text="Confirm 
Password:", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        confirm_password_label.grid(row=2, column=0, padx=10, pady=5, 
sticky="w") 
 
        self.reset_button = tk.Button(set_password_frame, text="Set Password", 
command=self.set_password, width=15, background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font) 
        self.reset_button.grid(row=3, column=0, columnspan=7, padx=10, pady=10, 
sticky="ew") 
 
        self.login_button = tk.Button(set_password_frame, text="Go to login", 
command=self.goto_login, state=tk.DISABLED, width=15, 
font=self.manage_font.small_bold_heading_font) 
        self.login_button.grid(row=4, column=0, columnspan=7, padx=10, pady=5, 
sticky="ew") 
        self.login_button.bind("<Button-1>", lambda event, func=login_callback: 
func()) 
 
        self.error_labels = [] 
        self.success_frame = [] 
 
    def clear_success_message(self, event): 
        self.login_button.config(state=tk.DISABLED) 
         
    def clear_error_messages(self): 
        for label in self.error_labels: 
            label.destroy() 
        self.error_labels = [] 
        self.login_button.config(state=tk.DISABLED) 
 
    def display_error_messages(self): 
        individual_error_frame = tk.Frame(self) 
        individual_error_frame.place(relx=0.5, rely=0.155, anchor=tk.CENTER) 
        for error_string in self.error_strings: 
            error_label = tk.Label(individual_error_frame, text=f"\u26A0 
{error_string}", background="#D11A17", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font, width=200) 
            error_label.pack(fill="both", padx=10, pady=2, anchor="w") 
            self.error_labels.append(error_label) 
 
    def display_message(self, text, background_color): 
        message_frame = tk.Frame(self, background=background_color) 
        message_frame.place(relx=0.5, rely=0.375, anchor=tk.CENTER, width=940) 
        message_label = tk.Label(message_frame, text=text, 
background=background_color, foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        message_label.pack(padx=10, pady=5) 
         
    def set_password(self): 
        self.message_handler.destroy_messages() 
        self.clear_error_messages() 
         
        self.error_strings = [] 
        self.success_string = "" 
 
        new_password = self.password_entry.get() 
        confirm_password = self.confirm_password_entry.get() 
 
        self.error_strings = 
self.validate_credentials.validate_password(new_password, 1, 
str(confirm_password)) 
 
        if self.error_strings: 
            self.display_error_messages() 
        elif not self.error_strings: 
            # Password meets all constraints, set the new passwords   
            self.update_password(self.member_id, new_password) 
            self.login_button.config(state=tk.NORMAL) 
 
    def update_password(self, member_id, new_password): 
        try: 
            password_handler = PasswordHandler() 
            hashed_password, salt = 
password_handler.hash_and_store_password(new_password) 
            # Update the password for the provided member_id 
            self.cursor.execute(''' 
                UPDATE Members 
                SET Password = ?, Salt = ? 
                WHERE MemberID = ?; 
            ''', (hashed_password, salt, member_id)) 
 
            self.conn.commit() 
            self.conn.close() 
 
            success_string = "Success: \n\n \u2705 Password set successfully! \n"   

            self.message_handler.success_message(success_string) 

        except sqlite3.Error as e: 
            print("Error occurred:", e) 
 
    def goto_login(self): 
        self.controller.show_login() 
