import tkinter as tk 
from tkinter import ttk 
from gym_font import * 
import sqlite3 
import datetime 
from datetime import datetime, timedelta 
from gym_function_bank import * 
 
class GymMembershipPackagePage(tk.Tk): 
    def __init__(self, location_id, membership_duration, user_detail_callback): 
        super().__init__() 
        self.user_detail_callback = user_detail_callback 
         
        self.title("Gym Details") 
        self.geometry("800x600") 
         
        self.location_id = location_id 
 
        self.membership_duration = membership_duration 
 
        self.manage_font = ManageFont() 
        self.message_handler = MessageHandler(self)
 
        self.create_membership_page() 
        self.create_membership_table() 
 
    def fetch_membership_packages(self, location_id): 
        try: 
            conn = sqlite3.connect('FitZone.db') 
            cursor = conn.cursor() 
 
            cursor.execute(""" 
                SELECT MembershipPackages.PackageID, 
MembershipPackages.PackageName, MembershipPrices.Price, 
MembershipPackages.Description, MembershipDurations.DurationName, 
                MembershipDurations.NumberOfDays 
                FROM MembershipPackages 
                JOIN MembershipDurations ON MembershipPackages.LocationID = 
MembershipDurations.LocationID 
                JOIN MembershipPrices ON MembershipPackages.PackageID = 
MembershipPrices.PackageID AND MembershipDurations.DurationID = 
MembershipPrices.DurationID 
                WHERE MembershipDurations.DurationID = ? AND 
MembershipPackages.LocationID = ? 
            """, (self.membership_duration, self.location_id)) 
             
            membership_packages = cursor.fetchall() 
 
            self.membership_packages = membership_packages 
 
            cursor.execute(''' 
                SELECT FeatureName, IsIncluded 
                FROM MembershipPackagesFeatures 
                WHERE PackageID IN ( 
                    SELECT PackageID 
                    FROM MembershipPackages 
                    WHERE LocationID = ? 
                ) 
            ''', (self.location_id,)) 
            membership_features = cursor.fetchall() 
 
            conn.close() 
            return membership_packages, membership_features 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [], [] 
 
    def create_membership_page(self): 
        self.frame = ttk.Frame(self) 
        self.frame.pack(fill='both', expand=True)
 
        style = ttk.Style() 
        style.configure("TRadiobutton", 
font=self.manage_font.medium_letters_font) 
 
        # Create a canvas with a scrollbar 
        canvas = tk.Canvas(self.frame) 
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", 
command=canvas.yview) 
        self.scrollable_frame = ttk.Frame(canvas) 
 
        canvas.pack(side="left", fill="both", expand=True) 
        scrollbar.pack(side="right", fill="y") 
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        canvas.configure(yscrollcommand=scrollbar.set) 
 
        self.content_frame = tk.Frame(self.scrollable_frame) 
        self.content_frame.pack(fill=tk.X, pady=150) 
 
        ttk.Label(self.content_frame, text="Membership Options", width=100, 
font=self.manage_font.large_bold_heading_font).pack(anchor=tk.SW) 
         
        membership_options_frame = ttk.Frame(self.content_frame) 
        membership_options_frame.pack(fill=tk.X) 
 
        location_id = 1 
 
        membership_packages, membership_features = 
self.fetch_membership_packages(location_id) 
        self.membership_packages = membership_packages 
        self.membership_features = membership_features 
 
        membership_var = tk.StringVar() 
        membership_var.set(self.membership_packages[0][1]) 
 
        for i in range(len(self.membership_packages)): 
            package_name = self.membership_packages[i][1] 
            ttk.Radiobutton(membership_options_frame, text=package_name, 
variable=membership_var, value=package_name).pack(side=tk.LEFT, padx=5) 
            self.membership_description_frame = ttk.Frame(self.content_frame) 
            self.membership_description_frame.pack(pady=10, fill=tk.X) 
 
        ttk.Label(self.membership_description_frame, text="Membership 
Description:", font=self.manage_font.large_bold_letters_font).pack(anchor=tk.W) 
        description = self.membership_packages[0][3] 
        ttk.Label(self.membership_description_frame, text=description, 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W)
        tk.Button(self.content_frame, text="View Option", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF", command=lambda: 
self.update_membership_description(membership_var.get(), 
self.membership_packages, self.membership_features)).pack(pady=10) 
 
        ttk.Label(self.content_frame, text="Membership Features:", 
font=self.manage_font.large_bold_letters_font).pack(anchor=tk.W) 
 
        self.content_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def create_membership_table(self): 
        # Configure the style for the Treeview widget 
        tree_style = ttk.Style() 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
 
        membership_table = ttk.Treeview(self.content_frame, show='headings', 
style="Custom.Treeview") 
 
        membership_table['columns'] = tuple(["Feature"] + [package[1] for 
package in self.membership_packages]) 
 
        # Configure the headings with the custom style 
        membership_table.heading('Feature', text='Gym Feature', anchor='w') 
        for _, package_name, _, _, _, _ in self.membership_packages: 
            membership_table.heading(package_name, text=package_name, 
anchor='w') 
 
        feature_data = {} 
 
        for feature_name, is_included in self.membership_features: 
            if feature_name not in feature_data: 
                feature_data[feature_name] = [] 
            feature_data[feature_name].append("✔" if is_included else "✘") 
 
        combined_features = [[feature_name] + data for feature_name, data in 
feature_data.items()] 
 
        for index in range(len(combined_features)): 
            feature_row = combined_features[index] 
 
            if index % 2 == 0: 
                bg_color = "#FFE4B5"  # Odd rows 
            else:
                bg_color = "#FFFFFF"  # Even rows 
 
            # Insert the row into the membership_table with the specified 
background color 
            item = membership_table.insert('', 'end', values=feature_row, 
tags=(bg_color,)) 
            membership_table.tag_configure(bg_color, background=bg_color) 
 
        membership_table.pack(fill='both', expand=True) 
 
    def create_additional_details_frame(self): 
        self.additional_details_frame = ttk.Frame(self.content_frame, 
style='TFrame') 
        self.additional_details_frame.pack(fill='both', expand=True, pady=20) 
         
        ttk.Style().configure('AdditionalDetails.TFrame', background="#333333") 
        
self.additional_details_frame.configure(style='AdditionalDetails.TFrame') 
 
        ttk.Label(self.additional_details_frame, text=f"Membership package: 
{self.package_name} ({self.duration_name})", 
font=self.manage_font.large_bold_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
 
        ttk.Separator(self.additional_details_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        ttk.Label(self.additional_details_frame, text="Total Price:", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
        total_price = self.price 
        ttk.Label(self.additional_details_frame, text=f"${total_price}", 
font=self.manage_font.large_bold_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
 
        ttk.Separator(self.additional_details_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        ttk.Label(self.additional_details_frame, text="Description:", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
        description = "Your description here" 
        ttk.Label(self.additional_details_frame, text=description, 
font=self.manage_font.medium_letters_font, wraplength=600, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
 
        ttk.Separator(self.additional_details_frame, orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        ttk.Label(self.additional_details_frame, text="Start Date:", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
        self.start_date = datetime.date.today().strftime("%Y-%m-%d") 
        self.start_date_label = ttk.Label(self.additional_details_frame, 
text=self.start_date, font=self.manage_font.medium_letters_font, 
background="#333333", foreground="#FFFFFF") 
        self.start_date_label.pack(anchor=tk.W, padx=10) 
        tk.Button(self.additional_details_frame, text="Set Start Date", 
command=self.open_calendar_window, font=self.manage_font.smaller_letters_font, 
background="#333333", foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
 
        ttk.Separator(self.additional_details_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
        ttk.Label(self.additional_details_frame, text="End Date:", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W, padx=10) 
        self.end_date_label = ttk.Label(self.additional_details_frame, text="", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF") 
        self.end_date_label.pack(anchor=tk.W, padx=10) 
 
        self.calculate_end_date() 
 
    def create_additional_button_frame(self): 
        additional_button_frame = ttk.Frame(self.content_frame) 
        additional_button_frame.pack(side=tk.BOTTOM, pady=10) 
 
        # Select more gyms button 
        tk.Button(additional_button_frame, text="Select More Gyms", width=200, 
background="#FFE4B5", foreground="#000000", 
font=self.manage_font.small_bold_heading_font).grid(row=0, column=0, padx=10) 
 
        # Continue button 
        self.continue_button = tk.Button(additional_button_frame, 
text="Continue", width=200, background="#4CAF50", foreground="#000000", 
font=self.manage_font.small_bold_heading_font) 
        self.continue_button.grid(row=1, column=0, padx=10) 
        self.continue_button.bind("<Button-1>", lambda event, 
func=self.user_detail_callback: func()) 
         
    def open_calendar_window(self): 
        calendar_window = CalendarWindow(self, "Delay Start Date") 
 
    def update_start_date(self, selected_date): 
        if self.valid_date(selected_date): 
            self.start_date = selected_date 
            self.start_date_label.config(text=selected_date) 
        self.calculate_end_date() 
 
    def calculate_end_date(self): 
        if self.start_date: 
            selected_start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d") 
            one_month_later = selected_start_date + 
timedelta(days=self.package_number_of_days) 
            self.end_date_label.config(text=one_month_later.strftime("%Y-%m-%d")) 
 
    def update_membership_description(self, selected_package, membership_packages, membership_features): 
        for widget in self.membership_description_frame.winfo_children(): 
            widget.destroy() 
             
        for package_id, package_name, price, description, duration_name, numberofdays in membership_packages: 
            if package_name == selected_package: 
                self.package_id = package_id 
                self.package_name = package_name 
                self.price = price 
                self.selected_package = selected_package 
                self.duration_name = duration_name 
                self.package_number_of_days = numberofdays 
 
                ttk.Label(self.membership_description_frame, text="Membership 
Description:", font=self.manage_font.large_bold_letters_font).pack(anchor=tk.W) 
                ttk.Label(self.membership_description_frame, text=description, 
font=self.manage_font.medium_letters_font).pack(anchor=tk.W) 
                ttk.Label(self.membership_description_frame, text=f"From 
${price} a month", 
font=self.manage_font.large_bold_letters_font).pack(anchor=tk.W) 
                break 
 
        try: 
            # Destroy the entire additional_details_frame 
            self.additional_details_frame.destroy() 
             
            # Recreate the additional_details_frame 
            self.create_additional_details_frame() 
        except: 
            self.create_additional_details_frame() 
            self.create_additional_button_frame() 
 
    def valid_date(self, selected_date): 
        error_string= "" 
         
        # Get the current date 
        current_date = datetime.datetime.today() 
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d') 
         
        # The difference between the selected date and the current date 
        date_difference = selected_date - current_date 
         
        # Check if the selected date is not in the past and not more than 30 
days ahead for delay 
        if date_difference.days < -1: 
            error_string = "Error: \n\n \u26A0 Selected date cannot be the 
past." 
        elif date_difference.days > 30: 
             
            error_string = "Error: \n\n \u26A0 You cannot delay your membership 
for longer than 30 days." 
        else: 
            success_string = "Success: \n\n \u2705 Start date changed 
successfully!" 
 
        if error_string: 
            self.message_handler.invalid_message(error_string) 
            self.continue_button.config(state=tk.DISABLED) 
            return False 
        else: 
            self.message_handler.success_message(success_string) 
            self.continue_button.config(state=tk.NORMAL) 
            return True 
 
    def get_membership_price(self): 
        return self.price 
 
    def get_membership_package_id(self): 
        return self.package_id

