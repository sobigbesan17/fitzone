import sqlite3 
import tkinter as tk 
from tkinter import ttk 
from gym_font import * 
from gym_email_verification import EmailVerification 
from gym_function_bank import * 
import time 
 
class GymAccountVerification(tk.Tk): 
    def __init__(self, email, username, set_new_password_callback): 
        super().__init__() 
        self.email = email   
        self.username = username 
 
        self.verification_code_sent_time = time.time() 
         
        self.title("Account Verification Page") 
 
        self.verification_code = None 
 
        self.member_id="" 
 
        self.manage_font = ManageFont() 
 
        self.message_handler = MessageHandler(self) 
         
        self.code_fields = [0] * 6 
        self.code_entries = []  # Store code entry widgets 
 
        style = ttk.Style(self) 
        style.configure("TFrame", background="#333333", foreground="#FFFFFF") 
 
        verification_frame = tk.Frame(self, background="#333333") 
        verification_frame.place(relx=0.5, rely=0.385, anchor=tk.CENTER, 
width=940) 
 
        description_label = tk.Label(verification_frame, text="Account Verification", background="#333333", foreground="#FFFFFF", 
                                     font=self.manage_font.large_bold_heading_font) 
        description_label.grid(row=0, column=0, padx=10, pady=5, columnspan=6, 
sticky="w") 
 
        message_label = tk.Label(verification_frame, text=f"If your details are 
in our system, we will send you an email with the code to", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        message_label.grid(row=1, column=0, columnspan=6, padx=10, pady=5, 
sticky="w") 
 
        email_label = tk.Label(verification_frame, text=self.email, 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_underline_letters_font) 
        email_label.grid(row=1, column=5, padx=50, pady=5, sticky="w") 
 
        for i in range(6): 
            code_entry = ttk.Entry(verification_frame, name=f"code_entry_{i}", 
font=self.manage_font.larger_bold_letters_font, justify="center") 
            code_entry.grid(row=3, column=i, padx=5, pady=5, sticky="w", 
columnspan=1, ipady=10) 
            code_entry.config(width=3) 
            code_entry.bind("<FocusIn>", self.on_entry_click) 
            self.code_entries.append(code_entry) 
 
            validate_code_input = self.register(self.check_numeric_input) 
            code_entry.config(validate="key", 
validatecommand=(validate_code_input, "%P", 1)) 
             
        self.verify_button = tk.Button(verification_frame, text="Verify Code", 
command=self.validate_code, width=10, background="#FFE4B5", 
foreground="#000000", font=self.manage_font.small_bold_heading_font) 
        self.verify_button.grid(row=4, column=0, columnspan=7, padx=10, pady=10, 
sticky="ew") 
 
        not_received_label = tk.Label(verification_frame, text="Didn't receive an email?", 
                                      background="#333333", foreground="#FFFFFF", font=self.manage_font.medium_letters_font) 
        not_received_label.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 
5), sticky="w") 
 
        self.resend_label = tk.Label(verification_frame, text="Resend Email", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_underline_letters_font, cursor="hand2", 
compound="left") 
        self.resend_label.grid(row=5, column=2, padx=20, pady=(0, 5), 
sticky="e") 
        self.resend_label.bind("<Button-1>", lambda event: self.send_email())

 
        self.continue_button = tk.Button(self, text="Continue \u2192", 
command=self.goto_set_new_password, width=10, background="#4CAF50", 
foreground="#FFFFFF", font=self.manage_font.small_bold_heading_font) 
        self.continue_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER, 
width=940) 
        self.continue_button.config(state=tk.DISABLED) 
        self.continue_button.bind("<Button-1>", lambda event, 
func=set_new_password_callback: func()) 
 
        self.send_email() 
 
    def validate_code(self): 
        self.error_string = "" 
        self.success_string = "" 
        self.info_string = "" 
 
        code = "".join(entry.get() for entry in self.code_entries) 
        entered_codes = [entry.get() for entry in self.code_entries] 
 
        correct_code_format = all(code and len(code) == 1 for code in 
entered_codes) 
 
        if correct_code_format and code == self.verification_code: 
            if self.verification_code_sent_time is not None: 
                current_time = time.time() 
                time_difference = current_time - 
self.verification_code_sent_time 
                if time_difference > 600:  # 10 minutes as seconds 
                    self.error_string = "Error: \n\n \u26A0 Verification code 
has expired. Please request a new code. \n" 
                else: 
                    self.success_string = "Success: \n\n \u2705 Code 
verification successful! \n" 
        elif not correct_code_format: 
            self.error_string =  "Error: \n\n \u26A0 Please enter the six-digit 
verification code. \n" 
        else: 
            self.error_string =  "Error: \n\n \u26A0 Invalid code. Please try 
again. \n" 
 
        if self.error_string: 
            self.message_handler.invalid_message(self.error_string) 
 
        if self.success_string: 
            self.message_handler.success_message(self.success_string) 
            self.display_continue_button() 
            self.disable_inputs_after_verification()
 
    def on_entry_click(self, event): 
        entry = event.widget 
        index = int(entry.winfo_name()[-1]) 
        self.code_fields[index] = 1 
        entry.delete(0, "end") 
        entry.config(foreground='black') 
         
    def send_email(self): 
        email_verifier = EmailVerification() 
 
        self.verification_code_sent_time = time.time() 
 
        # Read the email description and title from password_reset.txt 
        file_path = 'password_reset_email.txt' 
        read_text = ReadText(file_path) 
        description = read_text.extract_description('Description:') 
        title = read_text.extract_description('Title:') 
     
        if self.check_valid_username_and_email(self.email, self.username): # 
Checks if username and email credentials are valid 
            self.verification_code = email_verifier.verify_email(self.email, 
title, description) 
        else: 
            self.verification_code = 
email_verifier.verify_email("FitZoneBot@gmail.com", title, description) 
        self.info_string = email_verifier.get_info_string() 
        self.message_handler.info_message(self.info_string) 
 
    def goto_set_new_password(self): 
        self.controller.show_set_new_password() 
 
    def check_valid_username_and_email(self, email, username): 
        try: 
            conn = sqlite3.connect('FitZone.db') 
            cursor = conn.cursor() 
 
            # Query the database for the provided username and email 
            cursor.execute(''' 
                SELECT MemberID FROM Members 
                WHERE Email = ? AND Username = ?; 
            ''', (email, username)) 
 
            # Fetch the record if the email and username exists 
            record = cursor.fetchone() 
 
            conn.close() 
            if record: 
                # Username and email match a record inside Member 
                self.member_id = record[0] 
                return True 
            else: 
                # Username and email fail to match any records inside Member 
                return False 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return False 
 
    def check_numeric_input(self, string, length): 
        return (string.isdigit() or string=="") and len(string) <= int(length) 
 
    def disable_inputs_after_verification(self):    
        self.verify_button.config(state=tk.DISABLED) 
        self.resend_label.unbind("<Button-1>") 
        self.resend_label.config(cursor="arrow") 
 
        for entry in self.code_entries: 
            entry.config(state=tk.DISABLED) 
 
    def display_continue_button(self): 
        self.continue_button.config(state=tk.NORMAL) 
 
    def get_member_id(self): 
        return self.member_id
