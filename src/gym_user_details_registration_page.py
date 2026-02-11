import tkinter as tk 
from tkinter import ttk 
from tkcalendar import Calendar, DateEntry 
from gym_font import ManageFont 
from gym_function_bank import * 
from gym_captcha_verification import * 
from tkinter import filedialog 
import datetime 
 
class GymDetailsRegistrationPage(tk.Tk): 
    def __init__(self, payment_registration_callback): 
        super().__init__() 
        self.payment_registration_callback = payment_registration_callback 
         
        self.title("Gym Details") 
        self.geometry("800x600") 
 
        self.manage_font = ManageFont() 
        self.password_handler = PasswordHandler() 
 
        self.validate_credentials = ValidateCredentials() 
        self.message_handler = MessageHandler(self) 
        self.captcha_validation = CaptchaVerification() 
 
        self.show_password = tk.BooleanVar(value=False) 
        self.agreed_terms_and_conditions = tk.BooleanVar(value=False) 
        self.email_notifications = tk.BooleanVar(value=False) 
 
        self.image_path = "" 
                 
        self.create_gym_details_page() 
 
        self.error_string = [] 
 
    def create_gym_details_page(self): 
        self.frame = ttk.Frame(self, style='TFrame') 
        self.frame.pack(fill='both', expand=True) 
        gender_var = "Female" 
 
        style = ttk.Style() 
        style.configure("TMenubutton", 
font=self.manage_font.medium_letters_font) 
         
        # Create a canvas with a scrollbar 
        canvas = tk.Canvas(self.frame) 
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview) 
        self.scrollable_frame = ttk.Frame(canvas) 
 
        canvas.pack(side="left", fill="both", expand=True) 
        scrollbar.pack(side="right", fill="y") 
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        canvas.configure(yscrollcommand=scrollbar.set) 
         
        self.gym_details_frame = ttk.Frame(self.scrollable_frame) 
        self.gym_details_frame.pack(anchor="center", fill=tk.Y, pady=120) 
 
        ttk.Label(self.gym_details_frame, text="Enter User Details", 
font=self.manage_font.large_bold_heading_font).grid(row=0, column=0, 
sticky=tk.W) 
 
        ttk.Label(self.gym_details_frame, text="Please enter your personal information to create your gym website account and get started on your fitness journey.", font=self.manage_font.medium_letters_font).grid(row=1, column=0, 
columnspan=2, sticky=tk.W) 
 
        # Labels and entry fields for user details 
        ttk.Label(self.gym_details_frame, text="First Name:", 
font=self.manage_font.medium_letters_font).grid(row=2, column=0, sticky=tk.W) 
        self.first_name_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.first_name_entry.grid(row=2, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Last Name:", 
font=self.manage_font.medium_letters_font).grid(row=3, column=0, sticky=tk.W) 
        self.last_name_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.last_name_entry.grid(row=3, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Username:", 
font=self.manage_font.medium_letters_font).grid(row=4, column=0, sticky=tk.W) 
        self.username_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.username_entry.grid(row=4, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Password:", 
font=self.manage_font.medium_letters_font).grid(row=5, column=0, sticky=tk.W) 
        self.password_entry = ttk.Entry(self.gym_details_frame, show='*', 
font=self.manage_font.medium_letters_font, width=50) 
        self.password_entry.grid(row=5, column=1, padx=10, pady=5) 
 
        show_password_checkbox = tk.Checkbutton(self.gym_details_frame, 
text="Show Password", font=self.manage_font.medium_letters_font, 
variable=self.show_password, command=self.toggle_password_visibility)
        show_password_checkbox.grid(row=5, column=2, padx=10, pady=5, 
sticky=tk.W) 
 
        ttk.Label(self.gym_details_frame, text="Email Address:", 
font=self.manage_font.medium_letters_font).grid(row=6, column=0, sticky=tk.W) 
        self.email_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.email_entry.grid(row=6, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Post Code:", 
font=self.manage_font.medium_letters_font).grid(row=7, column=0, sticky=tk.W) 
        self.postcode_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.postcode_entry.grid(row=7, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Phone Number:", 
font=self.manage_font.medium_letters_font).grid(row=8, column=0, sticky=tk.W) 
 
        # Dropdown menus for country code 
        country_code_var = tk.StringVar() 
        country_codes = ["+1", "+1", "+44", "+61", "+81", "+86"]   
        self.country_code_menu = ttk.OptionMenu(self.gym_details_frame, 
country_code_var, *country_codes) 
        self.country_code_menu.grid(row=8, column=1, padx=10, pady=5, 
sticky=tk.W) 
 
        self.phone_entry = ttk.Entry(self.gym_details_frame, width=45, 
font=self.manage_font.medium_letters_font) 
        self.phone_entry.grid(row=8, column=1, padx=10, pady=5, sticky=tk.E) 
 
        validate_phone_entry = self.register(self.check_numeric_input) 
        self.phone_entry.config(validate="key", 
validatecommand=(validate_phone_entry, "%P", 10)) 
 
        ttk.Label(self.gym_details_frame, text="Gender:", 
font=self.manage_font.medium_letters_font).grid(row=9, column=0, sticky=tk.W) 
        gender_var = tk.StringVar() 
        gender_options = ["Female", "Female", "Male", "Other"] 
        self.gender_menu = ttk.OptionMenu(self.gym_details_frame, gender_var, 
*gender_options) 
        self.gender_menu.grid(row=9, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Address:", 
font=self.manage_font.medium_letters_font).grid(row=10, column=0, sticky=tk.W) 
        self.address_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.address_entry.grid(row=10, column=1, padx=10, pady=5)
        ttk.Label(self.gym_details_frame, text="Date of Birth:", 
font=self.manage_font.medium_letters_font).grid(row=11, column=0, sticky=tk.W) 
        self.date_of_birth_entry = DateEntry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50, date_pattern="yyyy-MM-dd")  
# DateEntry for the Date of Birth 
        self.date_of_birth_entry.grid(row=11, column=1, padx=10, pady=5) 
 
        ttk.Label(self.gym_details_frame, text="Upload Profile Image:", 
font=self.manage_font.medium_letters_font).grid(row=12, column=0, sticky=tk.W) 
        self.image_label = tk.Label(self.gym_details_frame, text="🖼 \n Open Image", font=self.manage_font.medium_bold_letters_font, 
background="white",cursor="hand2", width=8, height=8) 
        self.image_label.grid(row=12, column=1, rowspan=8, padx=10, pady=10, 
sticky="ew") 
 
        self.image_label.bind("<Button-1>", self.upload_image) 
 
        self.captcha_image_label = ttk.Label(self.gym_details_frame) 
        self.captcha_image_label.grid(row=21, column=0, columnspan=2, pady=10) 
 
        self.user_captcha_entry = ttk.Entry(self.gym_details_frame, 
font=self.manage_font.medium_letters_font, width=50) 
        self.user_captcha_entry.grid(row=22, column=1, padx=10, pady=5) 
        self.user_captcha_entry.config(state="normal") 
        self.user_captcha_entry.insert(0, "Please enter CAPTCHA here") 
        self.user_captcha_entry.bind("<FocusIn>", self.on_entry_click) 
        self.user_captcha_entry.config(foreground='#888888') 
         
        self.captcha_image_label = ttk.Label(self.gym_details_frame) 
        self.captcha_image_label.grid(row=23, columnspan=2, pady=10) 
 
        self.refresh_captcha_button = tk.Button(self.gym_details_frame, 
text="Refresh CAPTCHA", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font, command=self.refresh_captcha_image) 
        self.refresh_captcha_button.grid(row=24, columnspan=2, pady=10) 
 
        self.submit_captcha_button = tk.Button(self.gym_details_frame, 
text="Submit CAPTCHA", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font, command=self.validate_captcha) 
        self.submit_captcha_button.grid(row=25, columnspan=2, pady=10) 
 
        show_email_notification_checkbox = tk.Checkbutton(self.gym_details_frame, text="I would like Email Notifications on Special Offers, Discounts, Benefits and Classes.", 
font=self.manage_font.smaller_letters_font, variable=self.email_notifications) 
        show_email_notification_checkbox.grid(row=26, column=1, padx=10, pady=5, sticky=tk.W)
        show_password_checkbox = tk.Checkbutton(self.gym_details_frame, text="I have read and agreed to the Terms and Conditions", 
font=self.manage_font.smaller_letters_font, 
variable=self.agreed_terms_and_conditions) 
        show_password_checkbox.grid(row=27, column=1, padx=10, pady=5, 
sticky=tk.W) 
         
        self.submit_button = tk.Button(self.gym_details_frame, text="Submit", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font, command=lambda: 
self.collect_user_details(gender_var, country_code_var)) 
        self.submit_button.grid(row=28, columnspan=2, pady=10) 
        self.submit_button.config(state=tk.DISABLED) 
 
        self.update_captcha_image()  
 
        self.scrollable_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def refresh_captcha_image(self): 
        self.captcha_validation.generate_captcha() 
        self.update_captcha_image() 
        self.user_captcha_entry.delete(0, tk.END) 
 
        self.user_captcha_entry.insert(0, "Please enter CAPTCHA here") 
        self.user_captcha_entry.bind("<FocusIn>", self.on_entry_click) 
        self.user_captcha_entry.bind("<FocusOut>", self.on_entry_click) 
        self.user_captcha_entry.config(foreground='#888888') 
 
    def update_captcha_image(self): 
        captcha_image_data = self.captcha_validation.get_captcha_image() 
        image = Image.open(BytesIO(captcha_image_data)) 
        image = ImageTk.PhotoImage(image) 
 
        self.captcha_image_label.config(image=image) 
        self.captcha_image_label.image = image 
 
    def collect_user_details(self, gender_var, country_code_var): 
        self.error_string = [] 
         
        # Retrieve the details entered by the user 
        self.first_name = self.first_name_entry.get() 
        self.last_name = self.last_name_entry.get() 
        self.username = self.username_entry.get() 
        self.password = self.password_entry.get() 
        self.email = self.email_entry.get() 
        self.post_code = self.postcode_entry.get() 
        self.country_code = country_code_var.get()
        self.phone_number = self.phone_entry.get() 
        self.gender = gender_var.get() 
        self.address = self.address_entry.get() 
        self.date_of_birth = self.date_of_birth_entry.get() 
 
        self.username_error_string = ""  
        self.password_error_string = "" 
        self.email_error_string = "" 
        self.date_of_birth_error_string = "" 
 
        self.collect_all_empty_fields() 
        self.username_error_string = self.validate_credentials.validate_username(self.username) 
        self.password_error_string = self.validate_credentials.validate_password(self.password, 0) 
        self.email_error_string = self.validate_credentials.validate_email(self.email) 
        self.phone_number_error_string = self.validate_credentials.validate_phone_number(self.phone_number) 
        self.date_of_birth_error_string = self.validate_credentials.validate_date_of_birth(self.date_of_birth) 
         
        self.destroy_error_messages() 
         
        if self.error_string: 
            self.display_error_messages(self.error_string)  
        elif self.username_error_string: 
            self.display_large_error_messages("Username", 
self.username_error_string) 
        elif self.password_error_string: 
            self.display_large_error_messages("Password", 
self.password_error_string) 
        elif self.email_error_string: 
            self.display_large_error_messages("Email", self.email_error_string) 
        elif self.phone_number_error_string: 
            self.display_large_error_messages("Phone Number", 
self.phone_number_error_string) 
        elif self.date_of_birth_error_string: 
            self.display_large_error_messages("Date Of Birth", 
self.date_of_birth_error_string) 
        elif not self.agreed_terms_and_conditions.get(): 
            self.display_large_error_messages("Terms & Conditions", "Please agree to the Terms & Conditions") 
        else: 
            self.submit_button.bind("<Button-1>", lambda event, 
func=self.payment_registration_callback: func()) 
            self.submit_button.event_generate("<Button-1>") 
             
    def validate_captcha(self): 
        user_input = self.user_captcha_entry.get() 
         
        error_string = "" 
        success_string = "" 
         
        if user_input.lower() == self.captcha_validation.get_captcha_text().lower(): 
            success_string = "Success: \n\n \u2705 CAPTCHA is correct!" 
 
            self.update_captcha_image() 
            self.user_captcha_entry.delete(0, tk.END) 
        else: 
            error_string = "Error: \n\n \u26A0 CAPTCHA is incorrect. Please try again." 
 
        if error_string: 
            self.message_handler.invalid_message(error_string) 
            self.submit_button.config(state=tk.DISABLED) 
        else: 
            self.message_handler.success_message(success_string) 
            self.submit_button.config(state=tk.NORMAL) 
            self.disable_captcha() 
 
    def disable_captcha(self): 
        self.submit_captcha_button.config(state=tk.DISABLED) 
        self.refresh_captcha_button.config(state=tk.DISABLED) 
        self.user_captcha_entry.config(state="disabled") 
 
         
    def destroy_error_messages(self): 
        try: 
            self.error_frame.destroy() 
        except: 
            None 
             
    def display_error_messages(self, error_string):       
        self.error_frame = tk.Frame(self.gym_details_frame) 
        self.error_frame.grid(row=29, column=1, padx=10, pady=10) 
         
        message_row = 0 
         
        for message in error_string: 
            message_row += 1 
            error_message_frame = tk.Frame(self.error_frame) 
            error_message_frame.grid(row=message_row, column=0, columnspan=2, 
sticky=tk.W, pady=5)   
             
            error_label = tk.Label(error_message_frame, text=message, font=self.manage_font.medium_letters_font, background="#D11A17", 
foreground="#FFFFFF", width=70) 
            error_label.pack(side="left") 
 
            close_button = tk.Button(error_message_frame, text="\u2716", 
background="#D11A17", foreground="#FFFFFF", command=lambda 
frame=error_message_frame: frame.destroy()) 
            close_button.pack(side="right") 
 
    def display_large_error_messages(self, error_title, error_string): 
        self.destroy_error_messages() 
        self.error_details_frame = tk.Frame(self.gym_details_frame) 
        self.error_details_frame.grid(row=29, column=1, padx=10, pady=10) 
 
        # Display error messages for empty fields 
        if error_string: 
            error_message_frame = tk.Frame(self.error_details_frame, 
background="#D11A17") 
            error_message_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, 
padx=10, pady=10)   
                 
            error_list = f"({error_title}) {error_string}" 
                 
            error_label = tk.Label(error_message_frame, text=error_list, 
font=self.manage_font.medium_letters_font, background="#D11A17", 
foreground="#FFFFFF", width=70) 
            error_label.pack(fill=tk.BOTH, expand=True) 
 
            close_button = tk.Button(error_message_frame, text="\u2716", 
background="#D11A17", foreground="#FFFFFF", command=lambda 
frame=error_message_frame: frame.destroy()) 
            close_button.pack(side="right") 
 
    def collect_all_empty_fields(self): 
        empty_fields = [] 
        self.error_string = [] 
 
        # Check for empty fields and add their names to the list 
        if not self.first_name: 
            empty_fields.append("First Name") 
        if not self.last_name: 
            empty_fields.append("Last Name") 
        if not self.username: 
            empty_fields.append("Username") 
        if not self.password: 
            empty_fields.append("Password") 
        if not self.email: 
            empty_fields.append("Email Address")
        if not self.post_code: 
            empty_fields.append("Post Code") 
        if not self.country_code: 
            empty_fields.append("Country Code") 
        if not self.phone_number: 
            empty_fields.append("Phone Number") 
        if not self.gender: 
            empty_fields.append("Gender") 
        if not self.address: 
            empty_fields.append("Address") 
        if not self.date_of_birth: 
            empty_fields.append("Date of Birth") 
 
        for fields in empty_fields: 
            self.error_string.append(f"Error: \u26A0 Please enter {fields}.") 
 
    def upload_image(self, event): 
        image_path = filedialog.askopenfilename(filetypes=[("Image files", 
"*.png *.jpg *.jpeg")]) 
        self.open_image(image_path) 
 
    def open_image(self, image_path): 
        self.image_path = "" 
        if image_path: 
            image = Image.open(image_path) 
            image = image.resize((200, 200), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image=image) 
 
            self.image_label.config(image=photo, width=100, height=200) 
            self.image_label.image = photo 
            self.image_path = image_path 
 
    def toggle_password_visibility(self): 
        if self.show_password.get(): 
            self.password_entry.config(show='')   
        else: 
            self.password_entry.config(show='*') 
 
        self.password_entry.focus_set() 
 
    def check_numeric_input(self, string, length): 
        return (string.isdigit() or string=="") and len(string) <= int(length) 
 
    def on_entry_click(self, event): 
        entry = event.widget 
        if entry.get() == "Please enter CAPTCHA here": 
            entry.delete(0, "end") 
            entry.insert(0, "")
            entry.config(foreground='black') 
 
    def get_user_account_details(self): 
        password_hash, salt = self.password_handler.hash_and_store_password(self.password) 
        join_date = datetime.datetime.now().date() 
        self.email_notifications_value = int(self.email_notifications.get()) 
     
        return [self.username, password_hash, salt, self.gender, self.email, 
self.date_of_birth, join_date, self.first_name, 
                self.last_name, self.address, self.country_code, 
self.phone_number, self.image_path, self.email_notifications_value]
