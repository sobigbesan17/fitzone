import tkinter as tk 
from tkinter import ttk 
import sqlite3 
from gym_font import * 
 
class GymMembershipDurationPage(tk.Tk): 
    def __init__(self, location_id, membership_package_callback): 
        super().__init__() 
        self.title("Membership Packages") 
        self.geometry("800x600") 
 
        self.membership_package_callback = membership_package_callback 
 
        self.location_id = location_id 
        self.package_price = 0 
 
        self.manage_font = ManageFont() 
         
        self.create_membership_page() 
        self.load_data() 
 
    def create_membership_page(self): 
        self.frame = ttk.Frame(self) 
        self.frame.pack(fill='both', expand=True) 
 
        # Create a canvas with a scrollbar 
        canvas = tk.Canvas(self.frame) 
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", 
command=canvas.yview) 
        self.scrollable_frame = ttk.Frame(canvas) 
 
        canvas.pack(side="left", fill="both", expand=True) 
        scrollbar.pack(side="right", fill="y") 
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        canvas.configure(yscrollcommand=scrollbar.set) 
         
        # Bind the canvas to update the scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
        self.duration_frame = tk.Frame(self.scrollable_frame) 
        self.duration_frame.pack(pady=160) 
         
    def load_data(self): 
        try: 
            conn = sqlite3.connect('FitZone.db') 
            cursor = conn.cursor() 
 
            # Fetch membership packages for FitZone Central 
            cursor.execute(''' 
                SELECT LocationName 
                FROM GymLocations 
                WHERE LocationID = ? 
            ''', (self.location_id,)) 
            self.location_name = cursor.fetchone()[0] 
 
            # Fetch membership packages for FitZone Central 
            cursor.execute(''' 
                SELECT DurationID, DurationName, Description 
                FROM MembershipDurations 
                WHERE LocationID = ? 
            ''', (self.location_id,)) 
            membership_packages = cursor.fetchall() 
 
            cursor.execute(''' 
                SELECT DailyPriceID, NumberOfDays, Price 
                FROM DailyPrices 
                WHERE LocationID = ? 
            ''', (self.location_id,)) 
            daily_prices = cursor.fetchall() 
 
            cursor.execute(''' 
                SELECT MIN(Price) 
                FROM DailyPrices 
                WHERE LocationID = ? 
            ''', (self.location_id,)) 
            self.lowest_daily_price = cursor.fetchone()[0] 
 
            cursor.execute(""" 
                SELECT MIN(Price) 
                FROM MembershipPrices 
                WHERE PackageID IN ( 
                    SELECT PackageID 
                    FROM MembershipPackages 
                    WHERE LocationID = ?
                ) 
            """, (self.location_id,)) 
            self.lowest_membership_package_price = cursor.fetchone()[0] 
 
            conn.close() 
 
            self.display_items(daily_prices, "Daily Prices") 
            self.display_items(membership_packages, "Membership Packages") 
 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
 
 
    def get_cheapest_duration_price(self, duration): 
        conn = sqlite3.connect('FitZone.db') 
        cursor = conn.cursor() 
         
        cursor.execute(''' 
            SELECT MIN(MembershipPrices.Price) CheapestPrice 
            FROM MembershipPackages 
            JOIN MembershipPrices ON MembershipPackages.PackageID = 
MembershipPrices.PackageID 
            JOIN MembershipDurations ON MembershipPrices.DurationID = 
MembershipDurations.DurationID 
            WHERE MembershipDurations.DurationName = ? AND 
MembershipDurations.LocationID = ?; 
        ''', (duration, 1)) 
 
        cheapest_price_result = cursor.fetchone()[0] 
        conn.close() 
 
        return cheapest_price_result 
 
    def display_items(self, items, title): 
        if title == "Daily Prices": 
            tk.Label(self.duration_frame, text=f"BUY MEMBERSHIP PACKAGE | 
{self.location_name}", 
font=self.manage_font.medium_letters_font).pack(anchor=tk.CENTER, padx=10, 
pady=10) 
 
            tk.Label(self.duration_frame, text=title, width=100, 
font=self.manage_font.large_bold_heading_font).pack(anchor=tk.W, padx=80, 
pady=10) 
             
            tk.Label(self.duration_frame, text=f"Enjoy the day passes from 
${self.lowest_daily_price}", 
font=self.manage_font.large_bold_letters_font).pack(anchor=tk.CENTER, padx=10, 
pady=10)
        else: 
            tk.Label(self.duration_frame, text=title, width=100, 
font=self.manage_font.large_bold_heading_font).pack(anchor=tk.W, padx=80, 
pady=10) 
             
            tk.Label(self.duration_frame, text=f"Enjoy the membership packages 
from ${self.lowest_membership_package_price}", 
font=self.manage_font.large_bold_letters_font).pack(anchor=tk.CENTER, padx=10, 
pady=10)         
 
        item_frame = tk.Frame(self.duration_frame)  # Create a separate frame to 
hold the boxes 
        item_frame.pack(anchor=tk.W, padx=10, pady=10, fill='both') 
 
        row = 0 
        col = 0 
        num_columns = 3 if title != "Daily Prices" else 4  
 
        for item in items: 
            if col == num_columns: 
                row += 1 
                col = 0 
 
            box_frame = tk.Frame(item_frame, relief='solid', 
background="#FFFFFF") 
            box_frame.grid(row=row, column=col, padx=10, pady=10) 
             
            if title == "Daily Prices": 
                number_of_days_id, item_name, price = item 
 
                number_of_day = item_name 
                rounded_price = format(price, '.2f') 
 
                average_price_per_day =  format(price/number_of_day, '.2f') 
 
                daily_string = f"{number_of_day} days" if item_name >= 2 else 
f"{item_name} day" 
                 
                tk.Label(box_frame, text=daily_string, 
font=self.manage_font.large_bold_heading_font, 
background="#FFFFFF").pack(anchor=tk.CENTER) 
                tk.Label(box_frame, text=f"${average_price_per_day} per day", 
font=self.manage_font.medium_bold_letters_font, background="#FFFFFF", 
foreground="#82B366").pack(anchor=tk.CENTER) 
                tk.Label(box_frame, text=f"Price: $" + str(rounded_price), 
font=self.manage_font.large_bold_letters_font, 
background="#FFFFFF").pack(anchor=tk.CENTER)  # Display the price for both daily prices and membership packages 
 
                tk.Button(box_frame, text="Choose", command=lambda id_value = 
number_of_days_id, name=daily_string, price_value=price: 
self.select_package(id_value, 0, name, price_value), 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.E) 
            else: 
                duration_id, item_name, description = item 
 
                from_price = self.get_cheapest_duration_price(item_name) 
      
                tk.Label(box_frame, text=item_name, 
font=self.manage_font.large_bold_heading_font, width=35, 
background="#FFFFFF").pack(anchor=tk.W) 
                 
                tk.Label(box_frame, text=description, 
font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF").pack(anchor=tk.W)  # Display the description for 
membership packages 
 
                tk.Label(box_frame, text=f"From $" + str(from_price), 
font=self.manage_font.large_bold_letters_font, 
background="#FFFFFF").pack(anchor=tk.W)  # Display the price for both daily 
prices and membership packages 
                tk.Button(box_frame, text="Choose", command=lambda id_value = 
duration_id, name=item_name, price_value=from_price: self.select_package(0, 
id_value, name, price_value), font=self.manage_font.medium_letters_font, 
background="#333333", foreground="#FFFFFF").pack(anchor=tk.E) 
 
            col += 1 
 
    def select_package(self, number_of_days_id, duration_id, package_name, 
package_price): 
        try: 
            self.box_frame.destroy() 
        except: 
            None 
 
        self.membership_number_of_days_id = number_of_days_id  
        self.membership_duration_id = duration_id 
        self.package_price = package_price 
         
        self.box_frame = tk.Frame(self.duration_frame, background="#333333") 
        self.box_frame.pack(padx=10, pady=10) 
 
        tk.Label(self.box_frame, text=f"Your selected membership plan: 
{package_name}", font=self.manage_font.large_bold_letters_font, 
background="#333333", foreground="#FFFFFF").pack(anchor=tk.W)
        tk.Label(self.box_frame, text=f"From ${package_price}", 
font=self.manage_font.medium_letters_font, background="#333333", 
foreground="#FFFFFF").pack(anchor=tk.W) 
         
        self.continue_button = tk.Button(self.box_frame, text="Continue", 
width=200, background="#4CAF50", foreground="#000000", 
font=self.manage_font.small_bold_heading_font) 
        self.continue_button.pack(anchor=tk.CENTER) 
        self.continue_button.bind("<Button-1>", lambda event, 
func=self.membership_package_callback: func()) 
 
    def get_membership_duration_id(self): 
        return self.membership_duration_id 
 
    def get_membership_number_of_days_id(self): 
        return self.membership_number_of_days_id 
 
    def get_membership_price(self): 
        return self.package_price 
