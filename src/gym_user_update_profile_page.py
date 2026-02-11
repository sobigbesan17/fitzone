import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from PIL import Image, ImageTk 
from tkinter import filedialog 
from gym_function_bank import * 
 
class GymUpdateProfile(tk.Tk): 
    def __init__(self, member_id): 
        super().__init__() 
        self.title("Gym Update Profile") 
        self.geometry("800x600") 
 
        self.member_id = member_id 
 
        self.manage_font = ManageFont() 
 
        self.message_handler = MessageHandler(self)
 
        self.conn = sqlite3.connect('FitZone.db') 
        self.cursor = self.conn.cursor()  
 
        self_member_current_username = None 
        self.error_string = None 
        self.success_string = None 
 
        self.create_profile_fields() 
        self.create_update_buttons() 
        self.load_user_details()  # Load user details from the database 
 
    def create_profile_fields(self): 
        self.profile_frame = ttk.Frame(self) 
        self.profile_frame.pack(pady=20) 
 
        update_profile_label = tk.Label(self.profile_frame, text="Update Profile", font=self.manage_font.heading_font) 
        update_profile_label.grid(row=0, column=0, columnspan=2, pady=30) 
 
        fields = ["Username", "Gender", "Email", "Date of Birth", "First Name", 
"Last Name", "Address", "Phone Number", "Image Path"] 
 
        self.entry_vars = {} 
        index = 0 
        for field in fields: 
            index += 1 
            label = tk.Label(self.profile_frame, text=field, 
font=self.manage_font.medium_letters_font) 
            label.grid(row=index + 1, column=0, padx=10, pady=5) 
 
            entry_var = tk.StringVar() 
 
            if field != "Image Path": 
                if index == 1: 
                    entry = tk.Entry(self.profile_frame, textvariable=entry_var, 
font=self.manage_font.medium_letters_font, state='disabled')  # Set font 
                else: 
                    entry = tk.Entry(self.profile_frame, textvariable=entry_var, 
font=self.manage_font.medium_letters_font)  # Set font 
 
                entry.grid(row=index + 1, column=1, padx=10, pady=5) 
 
                self.entry_vars[field] = entry_var 
            else: 
                self.image_label = tk.Label(self.profile_frame, text="🖼 \n Open Image", background="white", cursor="hand2", width=8, height=8) 
                self.image_label.grid(row=index + 1, column=1, rowspan=8, padx=10, pady=10, sticky="ew") 
 
                self.image_label.bind("<Button-1>", self.upload_image) 
 
    def create_update_buttons(self): 
        update_frame = ttk.Frame(self) 
        update_frame.pack(pady=20) 
 
        update_button = tk.Button(update_frame, text="Update Profile Account", 
background="#FFE4B5", font=self.manage_font.medium_letters_font, 
command=self.update_profile) 
        update_button.grid(row=0, column=0, padx=10, pady=5) 
 
    def load_user_details(self): 
        # Fetch user details from the database for member 
        self.cursor.execute(''' 
            SELECT Username, Gender, Email, DateOfBirth, FirstName, LastName, 
Address, PhoneNumber, ImagePath 
            FROM Members 
            WHERE MemberID = ?; 
        ''', (self.member_id,)) 
        user_details = self.cursor.fetchone() 
 
        if user_details: 
            fields = ["Username", "Gender", "Email", "Date of Birth", "First Name", "Last Name", "Address", "Phone Number", "Image Path"] 
            index = 0 
            for field in fields: 
                if field != "Image Path": 
                    self.entry_vars[field].set(user_details[index]) 
                else: 
                    self.open_image(user_details[index]) 
                index += 1 
 
    def update_profile(self): 
        # Get values from entry fields 
        gender = self.entry_vars["Gender"].get() 
        email = self.entry_vars["Email"].get() 
        dob = self.entry_vars["Date of Birth"].get() 
        first_name = self.entry_vars["First Name"].get() 
        last_name = self.entry_vars["Last Name"].get() 
        address = self.entry_vars["Address"].get() 
        phone_number = self.entry_vars["Phone Number"].get() 
        image_path = self.image_path 
 
        try: 
            # Update the database with the new values for member ID 1 
            self.cursor.execute('''
                            UPDATE Members 
                SET Username = ?, Gender = ?, Email = ?, DateOfBirth = ?, 
                    FirstName = ?, LastName = ?, Address = ?, PhoneNumber = ?, 
ImagePath = ? 
                WHERE MemberID = ?; 
                ''', (username, gender, email, dob, first_name, last_name, 
address, phone_number, image_path, self.member_id)) 
            self.conn.commit() 
 
            self.success_string = "Success: \n\n \u2705 User profile updated successfully." 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return None  # Return None in case of an error 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
         
        self.load_user_details()  # Reload user details after updating 
 
    def upload_image(self, event): 
        image_path = filedialog.askopenfilename(filetypes=[("Image files", 
"*.png *.jpg *.jpeg")]) 
        self.open_image(image_path) 
 
    def open_image(self, image_path): 
        if image_path: 
            self.image_path = image_path 
            image = Image.open(image_path) 
            image = image.resize((200, 200), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image=image) 
 
            self.image_label.config(image=photo, width=100, height=200) 
            self.image_label.image = photo 
 
if __name__ == "__main__": 
    app = GymUpdateProfile(1) 
    app.mainloop()
