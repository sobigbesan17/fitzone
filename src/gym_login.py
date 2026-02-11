import sqlite3 
import tkinter as tk 
from tkinter import ttk, messagebox 
import bcrypt 
from gym_font import * 
from gym_function_bank import * 
 
class GymLogin(tk.Tk): 
    def __init__(self, select_your_gym_callback, forgot_password_callback, 
successful_login_callback, message_error=None): 
        super().__init__() 
        self.successful_login_callback = successful_login_callback 
 
        self.manage_font = ManageFont() 
 
        self.message_handler = MessageHandler(self) 
 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor() 
 
        self.password_field=0 
        self.username_field=0 
 
        style = ttk.Style(self) 
        style.configure("TFrame", background="#333333", foreground="#FFFFFF") 
 
        login_frame = tk.Frame(self, background="#333333") 
        login_frame.place(relx=0.5, rely=0.37, anchor=tk.CENTER) 
 
        sign_up_description = tk.Label(login_frame, text="Log Into Your Account", background="#333333", foreground="#FFFFFF", font=self.manage_font.large_bold_heading_font) 
        sign_up_description.grid(row=0, column=0, padx=10, pady=5, columnspan=3, 
sticky="w") 
 
        sign_up_label = tk.Label(login_frame, text="Do not have an account?", 
background="#333333", foreground="#FFFFFF", font=self.manage_font.medium_letters_font) 
        sign_up_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 5), 
sticky="w") 
 
        sign_up_here_label = tk.Label(login_frame, text="Sign up here", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_underline_letters_font, cursor="hand2", 
compound="left") 
        sign_up_here_label.grid(row=1, column=1, padx=90, pady=(0, 5), 
sticky="w") 
        sign_up_here_label.bind("<Button-1>", lambda event: 
select_your_gym_callback()) 
 
        label_username = tk.Label(login_frame, text="Username:", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        label_username.grid(row=2, column=0, padx=10, pady=5, sticky="e") 
        self.entry_username = ttk.Entry(login_frame, name="username_entry", 
width=60, font=self.manage_font.medium_letters_font) 
        self.entry_username.grid(row=2, column=1, padx=10, pady=5) 
        self.entry_username.insert(0, "Enter your username") 
        self.entry_username.bind("<FocusIn>", self.on_entry_click) 
        self.entry_username.config(foreground='#888888') 
 
        label_password = tk.Label(login_frame, text="Password:", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        label_password.grid(row=3, column=0, padx=10, pady=5, sticky="e") 
        self.entry_password = ttk.Entry(login_frame, name="password_entry", 
width=60, show="*", font=self.manage_font.medium_letters_font) 
        self.entry_password.grid(row=3, column=1, padx=10, pady=5) 
        self.entry_password.insert(0, "Enter your password") 
        self.entry_password.bind("<FocusIn>", self.on_entry_click) 
        self.entry_password.config(foreground='#888888') 
 
        self.show_password_var = tk.BooleanVar() 
        self.show_password_var.set(False) 
        show_password_label = ttk.Label(login_frame, text="Show Password", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        show_password_label.grid(row=3, column=2, padx=5, pady=5) 
 
        show_password_checkbox = tk.Checkbutton(login_frame, 
variable=self.show_password_var, background="#333333", 
font=self.manage_font.medium_letters_font, 
command=self.toggle_password_visibility) 
        show_password_checkbox.grid(row=3, column=3, padx=5, pady=5) 
 
        forgot_password_label = tk.Label(login_frame, text="Forgot Password?", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_underline_letters_font, cursor="hand2", 
compound="left") 
        forgot_password_label.grid(row=4, column=0, padx=10, pady=5, 
columnspan=3, sticky="ew") 
        forgot_password_label.bind("<Button-1>", lambda event: 
forgot_password_callback())  # Bind a function to the label click 
 
        self.login_button = tk.Button(login_frame, text="Login", 
command=self.validate_login_inputs, width=10, background="#FFE4B5", 
foreground="#000000", font=self.manage_font.small_bold_heading_font) 
        self.login_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, 
sticky="ew") 
 
        if message_error: 
            self.message_handler.invalid_message(message_error) 
 
    def validate_login_inputs(self): 
        username = self.entry_username.get() 
        password = self.entry_password.get() 
 
        error_string="" 
 
        if (username and password) and self.username_field==1 and self.password_field==1: 
            self.member_id = self.validate_credentials(username, password) 
            if self.member_id: # Checks if username and password are valid records 
                success_message = "Success: \n\n \u2705 Login successful! You will be redirected shortly." 
            else: 
                error_string = "Error: \n\n \u26A0 Invalid username or password" 
        else: 
            if self.username_field==1 and username: 
                error_string = "Error: \n\n \u26A0 Please enter password." 
            elif self.password_field==1 and password: 
                error_string = "Error: \n\n \u26A0 Please enter username." 
            else: 
                error_string = "Error: \n\n \u26A0 Please enter both username and password." 
             
        if error_string: 
            self.message_handler.invalid_message(error_string) 
        else: 
            self.message_handler.success_message(success_message) 
            self.after(3000, self.perform_success) 
 
    def perform_success(self):
        self.login_button.bind("<Button-1>", lambda event, 
func=self.successful_login_callback: func()) 
        self.login_button.event_generate("<Button-1>") 
 
    def toggle_password_visibility(self): 
        if self.show_password_var.get(): 
            self.entry_password.config(show="") 
        else: 
            self.entry_password.config(show="*") 
 
    def on_entry_click(self, event): 
        entry = event.widget 
        if entry.get() == "Enter your username": 
            self.username_field=1 
            entry.delete(0, "end") 
            entry.insert(0, "") 
            entry.config(foreground='black') 
        elif entry.get() == "Enter your password": 
            self.password_field=1 
            entry.delete(0, "end") 
            entry.insert(0, "") 
            entry.config(foreground='black') 
 
    def validate_credentials(self, username, password): 
        try: 
            # Query the database for the provided username and password 
            self.cursor.execute(''' 
                SELECT MemberID, Password, Salt FROM Members 
                WHERE Username = ?; 
            ''', (username,)) 
 
            # Fetch the record if the username exists 
            record = self.cursor.fetchone() 
 
            if record: 
                # Check if the provided password matches the stored hash 
                member_id, stored_password_hash, salt = record 
                 
                password_handler = PasswordHandler() 
                provided_password_hash = password_handler.hash_password(password, salt) 
                if provided_password_hash == stored_password_hash: 
                    return member_id  # Credentials are valid, return the MemberID 
                else: 
                    return None  # Password doesn't match 
            else: 
                return None  # Username doesn't exist 
            conn.close() 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None 
 
    def get_member_id(self): 
        return self.member_id 
 
    def get_location_id(self): 
        self.cursor.execute(f"SELECT LocationID FROM Members WHERE MemberID = ?", (self.member_id,)) 
        location_id = self.cursor.fetchone()[0] 
 
        return location_id
