import tkinter as tk 
from tkinter import ttk, messagebox 
import sqlite3 
from tkcalendar import Calendar 
from datetime import datetime, timedelta 
from datetime import datetime 
from gym_font import ManageFont 
from gym_user_dropdown_menu import * 
from gym_function_bank import MessageHandler 
from PIL import Image, ImageTk 
from tkinter import filedialog 
from gym_meal_recommendation_algorithm import * 
 
class GymPersonalisedMealPlanner(tk.Tk): 
    def __init__(self, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback): 
        super().__init__() 
        self.title("Gym Personalised Meals Planner") 
        self.geometry("800x600") 
        self.error_frame = None 
        self.add_meal_frame = None 
        self.add_meal_title = None 
        self.remove_meal_frame = None 
        self.remove_meal_title = None 
        self.select_meal_frame = None 
        self.select_meal_title = None 
        self.custom_meal_frame = None 
        self.personalised_meal_frame = None 
        self.personalised_meal_title = None
        self.meal_recommendation_frame = None 
        self.member_id = member_id 
 
        self.manage_font = ManageFont() 
        self.message_handler = MessageHandler(self) 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, gym_workout_planner_callback, 
view_class_schedule_callback, gym_class_booking_callback, 
gym_class_clashes_callback) 
        self.current_date = datetime.datetime.today().date() 
 
        self.conn = sqlite3.connect("FitZone.db") 
        self.cursor = self.conn.cursor() 
         
        self.error_string = "" 
        self.info_string = "" 
        self.success_string = "" 
 
        self.selected_date = self.current_date 
 
        self.image_path = "" 
 
        self.user_dropdown_menu.pack(fill="x")  
 
        self.canvas = tk.Canvas(self, background="white") 
        self.canvas.pack(fill="both", expand=True) 
 
        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", 
command=self.canvas.yview) 
        self.scrollbar.pack(side="right", fill="y") 
 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.bind("<Configure>", self.configure_canvas) 
 
        self.content_frame = ttk.Frame(self.canvas, style="TFrame") 
        self.canvas.create_window((0, 0), window=self.content_frame, 
anchor="nw") 
 
        self.add_content() 
 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def configure_canvas(self, event): 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def add_content(self): 
        self.title_label = tk.Label(self.content_frame, text="Personalised Meal Planner", font=self.manage_font.large_bold_heading_font, background="white") 
        self.title_label.pack(pady=10) 
 
        self.title_label = tk.Label(self.content_frame, text="Build your custom meal plan to help you achieve your fitness goals.", 
font=self.manage_font.medium_bold_letters_font, background="white") 
        self.title_label.pack(pady=10) 
 
        self.header_frame = tk.Frame(self.content_frame, background="#CCCCCC") 
        self.header_frame.pack(fill="both") 
 
        self.grid_view = None 
        self.list_view = None 
         
        self.prev_week_button = tk.Button(self.header_frame, text="Previous Week", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.prev_week) 
        self.prev_week_button.pack(side="left", padx=10, pady=10) 
 
        self.next_week_button = tk.Button(self.header_frame, text="Next Week", 
background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.next_week) 
        self.next_week_button.pack(side="right", padx=10, pady=10) 
 
        self.add_meal_button = tk.Button(self.header_frame, text="Add Meal", 
background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_add_meal) 
        self.add_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.remove_meal_button = tk.Button(self.header_frame, text="Remove Meal", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_remove_item) 
        self.remove_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.select_meal_button = tk.Button(self.header_frame, text="Select Meal", background="#FFE4B5", font=self.manage_font.medium_bold_letters_font, 
command=self.show_select_meal) 
        self.select_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.add_custom_meal_button = tk.Button(self.header_frame, text="Add Custom Meal", background="#FFE4B5", 
font=self.manage_font.medium_bold_letters_font, command=self.show_custom_meal) 
        self.add_custom_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.remove_custom_meal_button = tk.Button(self.header_frame, 
text="Remove Custom Meal", background="#FFE4B5", 
font=self.manage_font.medium_bold_letters_font, 
command=self.show_remove_custom_meal)

        self.remove_custom_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.custom_meal_button = tk.Button(self.header_frame, 
text="Personalised Meal Algorithm", background="#FFE4B5", 
font=self.manage_font.medium_bold_letters_font, 
command=self.show_get_personalised_meal) 
        self.custom_meal_button.pack(side="left", padx=10, pady=10) 
 
        self.format_frame = tk.Frame(self.content_frame, background="#FFFFFF") 
        self.format_frame.pack(fill="both") 
 
        self.grid_button = tk.Button(self.format_frame, text="Grid Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_grid_view) 
        self.grid_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E) 
 
        self.list_button = tk.Button(self.format_frame, text="List Format", 
background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.show_list_view) 
        self.list_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E) 
 
        self.selected_date = self.current_date 
 
        self.date_picker_frame = tk.LabelFrame(self.content_frame, 
font=self.manage_font.medium_bold_letters_font) 
        self.date_picker_frame.pack(padx=10, pady=10, fill="both", expand=True) 
         
        self.date_picker_label = tk.Label(self.date_picker_frame, text="Select Date:", font=self.manage_font.medium_bold_heading_font) 
        self.date_picker_label.pack(pady=5) 
 
        self.date_picker_calendar = Calendar(self.date_picker_frame, 
selectmode="day", date_pattern="y-mm-dd", 
font=self.manage_font.medium_bold_letters_font, command=self.goto_date) 
        self.date_picker_calendar.pack() 
 
        self.goto_date_button = tk.Button(self.date_picker_frame, text="Go to Date", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_bold_letters_font, command=self.goto_selected_date) 
        self.goto_date_button.pack(pady=5) 
 
        self.meal_schedule_canvas = tk.Canvas(self.content_frame, 
background="white",height=60) 
        self.meal_schedule_canvas.pack(fill="both", expand=True) 
 
        self.show_grid_view() 
 
        self.goto_selected_date()
 
    def clear_meal_schedule(self): 
        for widget in self.meal_schedule_canvas.winfo_children(): 
            widget.destroy() 
 
    def draw_meal_schedule(self): 
        self.clear_meal_schedule() 
 
        meal_schedule_data = self.get_week_meal_schedule(self.selected_date) 
 
        date_range = [self.selected_date + timedelta(days=i) for i in range(7)] 
        time_of_day = ["Breakfast", "Lunch", "Dinner"] 
 
        if self.current_view == "grid": 
            self.grid_view = tk.Frame(self.meal_schedule_canvas, 
background="white") 
            self.grid_view.pack(fill="both", expand=True) 
         
            for row in range(len(time_of_day)): 
                time = time_of_day[row] 
                row += 1 
                label = ttk.Label(self.grid_view, text=time, anchor="center", 
background="#333333", foreground="white", 
font=self.manage_font.medium_bold_heading_font) 
                label.grid(row=row, column=0, sticky="nsew") 
 
            for column in range(1, len(date_range) + 1): 
                label = ttk.Label(self.grid_view, text=date_range[column-1], 
anchor="center", background="#333333", foreground="white", 
font=self.manage_font.medium_bold_heading_font) 
                label.grid(row=0, column=column, sticky="nsew") 
 
            for column in range(1, len(date_range) + 1): 
                for row in range(len(time_of_day)): 
                    time = time_of_day[row] 
                    row += 1 
                    meals = self.get_meal_schedule_data(date_range[column-1], 
time, time) 
                    snacks = self.get_meal_schedule_data(date_range[column-1], 
f"{time} Snacks", "Snacks") 
                    drinks = self.get_meal_schedule_data(date_range[column-1], 
f"{time} Drinks", "Drinks") 
                    meal_text = "\n".join(meals) 
                    snacks_text = "\n".join(snacks) 
                    drinks_text = "\n".join(drinks) 
 
                    text_widget = tk.Text(self.grid_view, wrap="word", height=8, 
width=18, state="normal", font=self.manage_font.medium_bold_letters_font) 

                    text_widget.insert("1.0", f"Meals: \n {meal_text} \n\n Snacks: \n {snacks_text} \n Drinks:\n{drinks_text}") 
                    text_widget.config(state="disabled") 
                    text_widget.grid(row=row, column=column, sticky="nsew") 
 
        elif self.current_view == "list": 
            distinct_days = self.get_meal_schedule_days() 
 
            self.title_label = tk.Label(self.meal_schedule_canvas, text=f"From {self.selected_date}", font=self.manage_font.large_bold_heading_font, 
background="white") 
            self.title_label.pack(pady=10) 
 
            if not distinct_days: 
                tk.Label(self.meal_schedule_canvas, text="No meals recorded for the selected week.", anchor="center", background = "#FFFFFF", 
font=self.manage_font.medium_bold_letters_font).pack(anchor="center", 
fill="both", padx=10, pady=10) 
                tk.Label(self.meal_schedule_canvas, text="Please try another week or", background = "#FFFFFF", 
font=self.manage_font.smaller_letters_font).pack(anchor="center", fill="both", 
padx=10, pady=10) 
 
                message_label = tk.Button(self.meal_schedule_canvas, text="Add a meal", font=self.manage_font.medium_bold_letters_font, 
command=self.show_add_meal, background="#333333", foreground="#FFFFFF") 
                message_label.pack(anchor="center", padx=10, pady=10) 
             
            for day in distinct_days: 
                list_title_frame = tk.Frame(self.meal_schedule_canvas, 
background="#333333") 
                list_title_frame.pack(padx=0, pady=0) 
                 
                title_label = tk.Label(list_title_frame, text=f"Day: {day}", 
background="#333333", foreground="#FFFFFF", width=160, 
font=self.manage_font.medium_bold_heading_font) 
                title_label.pack(fill="both") 
 
                columns = ["Date", "Time", "Meals", "Snacks", "Drinks"] 
                list_view = ttk.Treeview(self.meal_schedule_canvas, 
columns=columns, style="Custom.Treeview", height=4) 
                list_view.pack(fill="both", expand=True) 
 
                list_view["columns"] = columns 
                list_view.heading("#1", text="Date") 
                list_view.heading("#2", text="Time") 
                list_view.heading("#3", text="Meals") 
                list_view.heading("#4", text="Snacks") 

                list_view.heading("#5", text="Drinks") 
 
                for time in time_of_day: 
                    meals = self.get_meal_schedule_data(day, time, time) 
                    snacks = self.get_meal_schedule_data(day, f"{time} Snacks", "Snacks") 
                    drinks = self.get_meal_schedule_data(day, f"{time} Drinks", "Drinks") 
                    list_view.insert("", "end", values=[day, time, 
"\n".join(meals), "\n".join(snacks), "\n".join(drinks)]) 
 
    def show_grid_view(self): 
        self.current_view = "grid" 
 
        self.clear_meal_schedule() 
        self.draw_meal_schedule() 
 
        self.meal_schedule_canvas.update_idletasks() 
 
    def show_list_view(self):  
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
        self.current_view = "list" 
        self.clear_meal_schedule() 
        self.draw_meal_schedule() 
 
        self.meal_schedule_canvas.update_idletasks() 
       
    def prev_week(self): 
        self.selected_date -= timedelta(days=7) 
        self.clear_meal_schedule() 
        self.draw_meal_schedule() 
 
    def next_week(self): 
        self.selected_date += timedelta(days=7) 
        self.clear_meal_schedule() 
        self.draw_meal_schedule() 
 
    def update_meal_schedule(self): 
        self.draw_meal_schedule() 
 
    def get_week_meal_schedule(self, start_date=None): 
        meal_schedule_data = {} 
        if start_date is None: 
            start_date = datetime.datetime.now().date() 
        for i in range(7): 
            current_date = start_date + timedelta(days=i) 
            meals = self.get_meal_schedules_for_date(current_date) 
            if meals: 
                meal_schedule_data[current_date] = {} 
                for meal_entry in meals: 
                    meal_list = meal_entry[0].split('\n') 
                    current_meal_time = None  
                    for meal in meal_list: 
                        parts = meal.split(":") 
                        if len(parts) == 2: 
                            time, meal_name = parts 
                            current_meal_time = time   
                            meal_schedule_data[current_date].setdefault(current_meal_time, 
[]).append(meal_name.strip()) 
                        elif current_meal_time: 
                            if "Snacks" in meal: 
                                snack = meal.split(":")[1] 
                                meal_schedule_data[current_date].setdefault(current_meal_time + " Snacks", 
[]).append(snack) 
                            elif "Drinks" in meal: 
                                drink = meal.split(":")[1] 
                                meal_schedule_data[current_date].setdefault(current_meal_time + " Drinks", 
[]).append(drink) 
        return meal_schedule_data 
 
    def goto_date(self): 
        selected_date = self.date_picker_calendar.get_date() 
        try: 
            self.selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date() 
            self.update_meal_schedule() 
        except ValueError: 
            self.error_string = f"Error: \n\n \u26A0 Invalid date. Please select a valid date in the format YYYY-MM-DD." 
 
    def goto_selected_date(self): 
        selected_date_str = self.date_picker_calendar.get_date() 
        try: 
            self.selected_date = datetime.datetime.strptime(selected_date_str, 
"%Y-%m-%d").date() 
            self.update_meal_schedule() 
        except ValueError: 
            self.error_string = f"Error: \n\n \u26A0 Invalid date. Please select a valid date in the format YYYY-MM-DD." 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
 
    def add_meal(self, date, meal_type, meal_name=None, snack=None, drink=None): 
        try: 
            if meal_name or snack or drink: 
                item = True 
            else: 
                item = False 
 
            self.error_string = "" 
 
            if not date and not item: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a date and (meal, snack or drink)" 
            elif not item: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a meal, snack or drink" 
            elif not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a date" 
 
            if not self.error_string:             
                # Delete existing entries for the specified date and meal_type 
                self.cursor.execute("DELETE FROM MealSchedule WHERE Date = ? AND Time LIKE ?", 
                           (date, '%' + meal_type + '%')) 
               
                if meal_name: 
                    self.cursor.execute(''' 
                        INSERT INTO MealSchedule (MemberID, Date, Time, MealID, 
CustomMealID) 
                        SELECT ?, ?, ?,  
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN NULL ELSE (SELECT MealID FROM Meals WHERE 
MealName = ?) END, 
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN (SELECT CustomMealID FROM CustomMeals WHERE 
MealName = ?) ELSE NULL END 
                        ''', (self.member_id, date, meal_type, meal_name, 
meal_name, meal_name, meal_name)) 
 
                if snack: 
                    self.cursor.execute(''' 
                        INSERT INTO MealSchedule (MemberID, Date, Time, MealID, 
CustomMealID) 
                        SELECT ?, ?, ?,  
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN NULL ELSE (SELECT MealID FROM Meals WHERE 
MealName = ?) END, 
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN (SELECT CustomMealID FROM CustomMeals WHERE 
MealName = ?) ELSE NULL END 
                    ''', (self.member_id, date, meal_type + " Snacks", snack, 
snack, snack, snack)) 
 
 
                if drink: 
                    self.cursor.execute(''' 
                        INSERT INTO MealSchedule (MemberID, Date, Time, MealID, 
CustomMealID) 
                        SELECT ?, ?, ?,  
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN NULL ELSE (SELECT MealID FROM Meals WHERE 
MealName = ?) END, 
                               CASE WHEN (SELECT CustomMealID FROM CustomMeals 
WHERE MealName = ?) IS NOT NULL THEN (SELECT CustomMealID FROM CustomMeals WHERE 
MealName = ?) ELSE NULL END 
                    ''', (self.member_id, date, meal_type + " Drinks", drink, 
drink, drink, drink)) 
 
 
            self.conn.commit() 
            self.update_meal_schedule() 
 
            self.info_string = "Message: \n\n \u2139 Your item will be added if your input is valid." 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
     
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}") 
             
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.info_string:
                self.message_handler.info_message(self.info_string) 
 
    def remove_custom_meal_by_name(self, meal_name): 
        try: 
            self.cursor.execute("SELECT CustomMealID FROM CustomMeals WHERE MealName = ?", (meal_name,)) 
            delete_custom_meal = self.cursor.fetchall() 
 
            self.cursor.execute("DELETE FROM CustomMeals WHERE MealName = ?", (meal_name,)) 
 
            self.conn.commit() 
 
            self.success_string = "Success: \n\n \u2705 Your custom meal had been removed successfully!" 
            self.update_meal_schedule() 
                          
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while deleting the custom meal: {e}") 
            return False 
 
        finally: 
            if self.success_string and delete_custom_meal: 
                self.message_handler.success_message(self.success_string) 
                return 
 
            if not meal_name: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a meal name" 
            else: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a valid meal name" 
            self.message_handler.invalid_message(self.error_string) 
                
                 
    def remove_item(self, date, meal_type): 
        try: 
            if not meal_type and not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date and meal type" 
            elif not meal_type: 
                self.error_string = f"Error: \n\n \u26A0 Please enter meal type" 
            elif not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date"
            self.cursor.execute("DELETE FROM MealSchedule WHERE date = ? AND time LIKE ?", 
                       (date, '%' + meal_type + '%')) 
            self.conn.commit() 
             
            self.update_meal_schedule() 
            self.success_string = "Success: \n\n \u2705 Your meal had been added successfully!" 
      
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}") 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
   
    def view_meal_details(self, date, meal_type): 
        try: 
            meal_details = self.get_meal_schedule_data(date, meal_type, meal_type) 
            snack_details = self.get_meal_schedule_data(date, f"{meal_type} Snacks", "Snacks") 
            drink_details = self.get_meal_schedule_data(date, f"{meal_type} Drinks", "Drinks") 
 
            self.error_string = "" 
 
            if not meal_type and not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date and meal type" 
            elif not meal_type: 
                self.error_string = f"Error: \n\n \u26A0 Please enter meal type" 
            elif not date: 
                self.error_string = f"Error: \n\n \u26A0 Please enter date" 
            elif not (meal_details or snack_details or drink_details): 
                self.error_string = f"Error: \n\n \u26A0 An error occurred: No {meal_type} found for the {date}" 
 
            if not self.error_string: 
                ttk.Separator(self.select_meal_frame, 
orient="horizontal").pack(fill="x", padx=10, pady=5) 
 
                if meal_details: 
                    meal_text = "Main Meal:\n" + "\n".join(meal_details)

                    meal_label = ttk.Label(self.select_meal_frame, 
text=meal_text, font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
                    meal_label.pack(padx=10, pady=10) 
 
                if snack_details: 
                    snack_text = "Snacks:\n" + "\n".join(snack_details) 
                    snack_label = ttk.Label(self.select_meal_frame, 
text=snack_text, font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
                    snack_label.pack(padx=10, pady=10) 
 
                if drink_details: 
                    drink_text = "Drinks:\n" + "\n".join(drink_details) 
                    drink_label = ttk.Label(self.select_meal_frame, 
text=drink_text, font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
                    drink_label.pack(padx=10, pady=10) 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
     
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}") 
 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
     
    def update_meal_name_combo(self, meal_type_combo, meal_name_combo): 
        selected_meal_type = meal_type_combo.get() 
        meal_names = self.select_meals_by_type(selected_meal_type) 
        meal_name_combo["values"] = meal_names 
        meal_name_combo.set("") 
       
    def show_add_meal(self): 
        self.destroy_all_frames() 
         
        self.add_meal_title = tk.Frame(self, background="#000000") 
        self.add_meal_title.pack(padx=10, pady=0, anchor="center", fill="x") 
         
        tk.Label(self.add_meal_title, text="Add Meal", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
         
        self.add_meal_frame = tk.Frame(self, background="#333333")

        self.add_meal_frame.pack(padx=10, pady=0, anchor="center", fill="both") 
 
        close_button = tk.Button(self.add_meal_frame, text="\u2716", fg="white", 
bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.add_meal_frame, text="Date (YYYY-MM-DD):", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.add_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        meal_type_label = ttk.Label(self.add_meal_frame, text="Meal Type:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_type_label.pack(padx=10, pady=5) 
        meal_type_combo = ttk.Combobox(self.add_meal_frame, values=["Breakfast", 
"Lunch", "Dinner"], font=self.manage_font.medium_bold_letters_font, width=50) 
        meal_type_combo.pack(padx=10, pady=5) 
        meal_type_combo.bind("<<ComboboxSelected>>", lambda event: 
self.update_meal_name_combo(meal_type_combo, meal_name_combo)) 
 
        meal_name_label = ttk.Label(self.add_meal_frame, text="Meal Name:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_name_label.pack(padx=10, pady=5) 
        meal_name_combo = ttk.Combobox(self.add_meal_frame, values=[], 
font=self.manage_font.medium_bold_letters_font, width=50) 
        meal_name_combo.pack(padx=10, pady=5) 
        meal_name_combo.set("") 
 
        snack_label = ttk.Label(self.add_meal_frame, text="Snack:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        snack_label.pack(padx=10, pady=5) 
        snack_combo = ttk.Combobox(self.add_meal_frame, 
values=self.select_meals_by_type("Snacks"), 
font=self.manage_font.medium_bold_letters_font, width=50) 
        snack_combo.pack(padx=10, pady=5) 
        snack_combo.set("") 
 
        drink_label = ttk.Label(self.add_meal_frame, text="Drink:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        drink_label.pack(padx=10, pady=5) 
        drink_combo = ttk.Combobox(self.add_meal_frame, values=self.select_meals_by_type("Drinks"), 
font=self.manage_font.medium_bold_letters_font, width=50) 
        drink_combo.pack(padx=10, pady=5) 
        drink_combo.set("") 
 
        add_button = tk.Button(self.add_meal_frame, text="Add", 
font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: self.add_meal(date_entry.get(), 
meal_type_combo.get(), meal_name_combo.get(), snack_combo.get(), 
drink_combo.get())) 
        add_button.pack(padx=10, pady=10) 
 
    def show_remove_item(self): 
        self.destroy_all_frames() 
 
        self.remove_meal_title = tk.Frame(self, background="#000000") 
        self.remove_meal_title.pack(padx=10, pady=0, anchor="center", fill="x") 
         
        tk.Label(self.remove_meal_title, text="Remove Meal", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x")   
         
        self.remove_meal_frame = tk.Frame(self, background="#333333") 
        self.remove_meal_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
         
        close_button = tk.Button(self.remove_meal_frame, text="\u2716", 
fg="white", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.remove_meal_frame, text="Date (YYYY-MM-DD):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.remove_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        meal_type_label = ttk.Label(self.remove_meal_frame, text="Meal Type:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_type_label.pack(padx=10, pady=5) 
        meal_type_combo = ttk.Combobox(self.remove_meal_frame, 
values=["Breakfast", "Lunch", "Dinner"], 
font=self.manage_font.medium_bold_letters_font, width=50) 
        meal_type_combo.pack(padx=10, pady=5)

        remove_button = tk.Button(self.remove_meal_frame, text="Remove", 
font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.remove_item(date_entry.get(), meal_type_combo.get())) 
        remove_button.pack(padx=10, pady=10) 
 
    def show_select_meal(self): 
        self.destroy_all_frames() 
 
        self.select_meal_title = tk.Frame(self, background="#000000") 
        self.select_meal_title.pack(padx=10, pady=0, anchor="center", fill="x") 
         
        tk.Label(self.select_meal_title, text="Select Meal", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
         
         
        self.select_meal_frame = tk.Frame(self, background="#333333") 
        self.select_meal_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.select_meal_frame, text="\u2716", 
fg="white", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        date_label = ttk.Label(self.select_meal_frame, text="Date (YYYY-MM-DD):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        date_label.pack(padx=10, pady=5) 
        date_entry = ttk.Entry(self.select_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        date_entry.pack(padx=10, pady=5) 
 
        meal_type_label = ttk.Label(self.select_meal_frame, text="Meal Type:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_type_label.pack(padx=10, pady=5) 
        meal_type_combo = ttk.Combobox(self.select_meal_frame, 
values=["Breakfast", "Lunch", "Dinner"], 
font=self.manage_font.medium_bold_letters_font, width=50) 
        meal_type_combo.pack(padx=10, pady=5) 
 
        view_details_button = tk.Button(self.select_meal_frame, text="View Details", font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.view_meal_details(date_entry.get(), meal_type_combo.get())) 
        view_details_button.pack(padx=10, pady=10) 

 
    def show_custom_meal(self): 
        self.destroy_all_frames() 
 
        self.custom_meal_frame = tk.Frame(self, background="#333333") 
        self.custom_meal_frame.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        self.custom_meal_title = tk.Frame(self, background="#000000") 
        self.custom_meal_title.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        close_button = tk.Button(self.custom_meal_frame, text="\u2716", 
fg="white", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.grid(row=1, column=3, sticky="ne") 
 
        tk.Label(self.custom_meal_frame, text="Custom your own Fitness Meal", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF", width=120).grid(row=0, column=0, columnspan=6) 
 
        item_type_label = ttk.Label(self.custom_meal_frame, text="Item Type:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        item_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w") 
        item_type_combo = ttk.Combobox(self.custom_meal_frame, 
values=["Breakfast", "Lunch", "Dinner", "Snacks", "Drinks"], 
font=self.manage_font.medium_bold_letters_font, width=50) 
        item_type_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew") 
         
        item_name_label = ttk.Label(self.custom_meal_frame, text="Item Name:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        item_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w") 
        item_name_combo = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        item_name_combo.grid(row=3, column=1, padx=10, pady=5, sticky="ew") 
 
        item_summary_label = ttk.Label(self.custom_meal_frame, text="Item Summary:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        item_summary_label.grid(row=5, column=0, padx=10, pady=5, sticky="w") 
        item_summary_text = tk.Text(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50, height=9) 
        item_summary_text.grid(row=4, rowspan=9, column=1, padx=10, pady=5, 
sticky="ew") 
 
        calories_label = ttk.Label(self.custom_meal_frame, text="Calories (kcals):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 

        calories_label.grid(row=13, column=0, padx=10, pady=5, sticky="w") 
        calories_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        calories_entry.grid(row=13, column=1, padx=10, pady=5, sticky="ew") 
 
        validate_calories = self.register(self.check_numeric_input) 
        calories_entry.config(validate="key", 
validatecommand=(validate_calories, "%P", 4)) 
 
        protein_label = ttk.Label(self.custom_meal_frame, text="Protein (grams):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        protein_label.grid(row=14, column=0, padx=10, pady=5, sticky="w") 
        protein_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        protein_entry.grid(row=14, column=1, padx=10, pady=5, sticky="ew") 
 
        validate_protein = self.register(self.check_numeric_input) 
        protein_entry.config(validate="key", validatecommand=(validate_protein, 
"%P", 3)) 
 
        fat_label = ttk.Label(self.custom_meal_frame, text="Fat (grams):", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        fat_label.grid(row=15, column=0, padx=10, pady=5, sticky="w") 
        fat_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        fat_entry.grid(row=15, column=1, padx=10, pady=5, sticky="ew") 
 
        validate_fat = self.register(self.check_numeric_input) 
        fat_entry.config(validate="key", validatecommand=(validate_fat, "%P", 
3)) 
 
        carbohydrates_label = ttk.Label(self.custom_meal_frame, 
text="Carbohydrates (grams):", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        carbohydrates_label.grid(row=16, column=0, padx=10, pady=5, sticky="w") 
        carbohydrates_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=50) 
        carbohydrates_entry.grid(row=16, column=1, padx=10, pady=5, sticky="ew") 
 
        validate_carbohydrates = self.register(self.check_numeric_input) 
        carbohydrates_entry.config(validate="key", 
validatecommand=(validate_fat, "%P", 3)) 
 
        nutritional_goals_label = ttk.Label(self.custom_meal_frame, 
text="Nutritional Goals:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 

        nutritional_goals_label.grid(row=17, column=0, padx=10, pady=5, 
sticky="w") 
        nutritional_goals_combo = ttk.Combobox(self.custom_meal_frame, 
values=self.select_distinct_nutritional_goals(), 
font=self.manage_font.medium_bold_letters_font, width=50) 
        nutritional_goals_combo.grid(row=17, column=1, padx=10, pady=5, 
sticky="ew") 
 
        budget_label = ttk.Label(self.custom_meal_frame, text="Budget (£):", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        budget_label.grid(row=2, column=2, padx=10, pady=5, sticky="w") 
        budget_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        budget_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew") 
 
        validate_budget = self.register(self.check_numeric_input) 
        budget_entry.config(validate="key", validatecommand=(validate_budget, 
"%P", 3)) 
 
        dietary_restrictions_label = ttk.Label(self.custom_meal_frame, 
text="Dietary Restrictions:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        dietary_restrictions_label.grid(row=3, column=2, padx=10, pady=5, 
sticky="w") 
        dietary_restrictions_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        dietary_restrictions_entry.grid(row=3, column=3, padx=10, pady=5, 
sticky="ew") 
 
        allergies_label = ttk.Label(self.custom_meal_frame, text="Allergies:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        allergies_label.grid(row=4, column=2, padx=10, pady=5, sticky="w") 
        allergies_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        allergies_entry.grid(row=4, column=3, padx=10, pady=5, sticky="ew") 
 
        meal_size_label = ttk.Label(self.custom_meal_frame, text="Meal Size (g):", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_size_label.grid(row=5, column=2, padx=10, pady=5, sticky="w") 
        meal_size_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        meal_size_entry.grid(row=5, column=3, padx=10, pady=5, sticky="ew") 
 
        meal_size_fat = self.register(self.check_numeric_input) 
        meal_size_entry.config(validate="key", validatecommand=(validate_fat, "%P", 4)) 

 
        ingredients_label = ttk.Label(self.custom_meal_frame, 
text="Ingredients:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        ingredients_label.grid(row=6, column=2, padx=10, pady=5, sticky="w") 
        ingredients_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        ingredients_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew") 
 
        cooking_time_label = ttk.Label(self.custom_meal_frame, text="Cooking Time (minutes):", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        cooking_time_label.grid(row=7, column=2, padx=10, pady=5, sticky="w") 
        cooking_time_entry = ttk.Entry(self.custom_meal_frame, 
font=self.manage_font.medium_bold_letters_font, width=30) 
        cooking_time_entry.grid(row=7, column=3, padx=10, pady=5, sticky="ew") 
 
        validate_cooking_time = self.register(self.check_numeric_input) 
        cooking_time_entry.config(validate="key", 
validatecommand=(validate_cooking_time, "%P", 3)) 
 
        image_path_label = tk.Label(self.custom_meal_frame, text="Upload Item Image:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        image_path_label.grid(row=8, column=2, padx=10, pady=10, sticky="w") 
 
        self.image_label = tk.Label(self.custom_meal_frame, text="🖼 \n Open Image", font=self.manage_font.medium_bold_letters_font, 
background="white",cursor="hand2", width=8, height=8) 
        self.image_label.grid(row=8, column=3, rowspan=8, padx=10, pady=10, 
sticky="ew") 
 
        self.image_label.bind("<Button-1>", self.upload_image) 
 
        file_path_label = tk.Label(self.custom_meal_frame, text="Upload Item File:", font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        file_path_label.grid(row=16, column=2, padx=10, pady=10, sticky="w") 
 
        self.file_label = tk.Label(self.custom_meal_frame, text="📂\n Open File", font=self.manage_font.medium_bold_letters_font, 
background="white",cursor="hand2", width=8, height=8) 
        self.file_label.grid(row=16, column=3, rowspan=8, padx=10, pady=10, 
sticky="ew") 
 
        self.file_label.bind("<Button-1>", self.upload_file) 
 
        add_button = tk.Button(self.custom_meal_frame, text="Add", 

font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, 
                               command=lambda: 
self.add_item(item_name_combo.get(), 
                                                             
item_type_combo.get(), 
                                                             
item_summary_text.get("1.0", "end-1c"), 
                                                             
calories_entry.get(), 
                                                             
protein_entry.get(), 
                                                             fat_entry.get(), 
                                                             
carbohydrates_entry.get(), 
                                                             
ingredients_entry.get(), 
                                                             
cooking_time_entry.get(), 
                                                             self.image_path, 
                                                             "None")) 
        add_button.grid(row=18, column=0, columnspan=2, padx=10, pady=10, 
sticky="ew") 
 
    def show_remove_custom_meal(self): 
        self.destroy_all_frames() 
 
        self.remove_meal_title = tk.Frame(self, background="#000000") 
        self.remove_meal_title.pack(padx=10, pady=0, anchor="center", fill="x") 
 
        tk.Label(self.remove_meal_title, text="Remove Custom Meal", 
font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(padx=10, pady=0, fill="x") 
 
        self.remove_meal_frame = tk.Frame(self, background="#333333") 
        self.remove_meal_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        close_button = tk.Button(self.remove_meal_frame, text="\u2716", 
fg="white", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.place(relx=1, rely=0, anchor="ne") 
 
        custom_meal_name_label = ttk.Label(self.remove_meal_frame, text="Custom Meal Name:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
        custom_meal_name_label.pack(padx=10, pady=5) 
        custom_meal_name_combo = ttk.Combobox(self.remove_meal_frame, 
values=self.select_all_custom_meal(), font=self.manage_font.medium_bold_letters_font, width=50) 
        custom_meal_name_combo.pack(padx=10, pady=5) 
         
        remove_button = tk.Button(self.remove_meal_frame, text="Remove", 
font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: 
self.remove_custom_meal_by_name(custom_meal_name_combo.get())) 
        remove_button.pack(padx=10, pady=10) 
 
    def show_get_personalised_meal(self): 
        self.destroy_all_frames() 
 
        self.personalised_meal_frame = tk.Frame(self, background="#333333") 
        self.personalised_meal_frame.pack(padx=10, pady=0, anchor="center", 
fill="both") 
 
        canvas = tk.Canvas(self.personalised_meal_frame, width=600, height=600, 
background="#333333") 
        canvas.pack(side="left", fill="both", expand=True) 
 
        scrollbar = ttk.Scrollbar(self.personalised_meal_frame, 
orient="vertical", command=canvas.yview) 
        scrollbar.pack(side="right", fill="y") 
 
        canvas.configure(yscrollcommand=scrollbar.set) 
 
        self.frame_in_canvas = tk.Frame(canvas, background="#333333") 
         
        canvas.create_window((0, 0), window=self.frame_in_canvas, anchor="nw") 
 
        personalised_meal_title = tk.Frame(self.frame_in_canvas, 
background="#000000") 
        personalised_meal_title.grid(row=0, column=0, columnspan=6) 
 
        tk.Label(personalised_meal_title, text="Get Personalised Meal", 
width=115, font=self.manage_font.large_bold_heading_font, background="#000000", 
foreground="#FFFFFF").pack(fill="x") 
 
        close_button = tk.Button(self.frame_in_canvas, text="\u2716", 
fg="white", bg="red", font=self.manage_font.medium_letters_font, 
command=self.destroy_all_frames) 
        close_button.grid(row=1, column=4, sticky="ne") 
 
        row_num = 2  
        label_entries = [ 
            ("Calories (cal):", "calories_entry"), 
            ("Protein (g):", "protein_entry"), 
            ("Fat (g):", "fat_entry"),
            ("Carbohydrates (g):", "carbohydrates_entry"), 
            ("Ingredients:", "ingredients_entry"), 
            ("Cooking Time (minutes):", "cooking_time_entry"), 
            ("Nutritional Goals:", "nutritional_goals_entry"), 
            ("Budget (£):", "budget_entry"), 
            ("Dietary Restrictions:", "dietary_restrictions_entry"), 
            ("Allergies:", "allergies_entry"), 
            ("Meal Size (g):", "meal_size_entry") 
        ] 
 
        for label_text, entry_name in label_entries: 
            if row_num == 8: 
                nutritional_goals_label = ttk.Label(self.frame_in_canvas, 
text="Nutritional Goals:", font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#FFFFFF") 
                nutritional_goals_label.grid(row=19, column=0, padx=10, pady=5, 
sticky="w") 
                self.nutritional_goals_combo = ttk.Combobox(self.frame_in_canvas, 
values=self.select_distinct_nutritional_goals(), 
font=self.manage_font.medium_bold_letters_font, width=50) 
                self.nutritional_goals_combo.grid(row=19, column=1, padx=10, 
pady=5, sticky="ew") 
            else: 
                label = ttk.Label(self.frame_in_canvas, text=label_text, 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
                label.grid(row=row_num, column=0, padx=10, pady=5, sticky="w") 
 
                entry = ttk.Entry(self.frame_in_canvas, 
font=self.manage_font.medium_bold_letters_font, width=50) 
                setattr(self, entry_name, entry)  
                entry.grid(row=row_num, column=1, padx=10, pady=5) 
 
                if (entry_name == "calories_entry" or entry_name == 
"protein_entry" or entry_name == "fat_entry" or entry_name == 
"carbohydrates_entry" or entry_name == "cooking_time_entry" 
                    or entry_name == "budget_entry" or entry_name == 
"meal_size_entry"): 
                    validate_entry = self.register(self.check_numeric_input) 
                    entry.config(validate="key", 
validatecommand=(validate_entry, "%P", 3)) 
                     
            row_num += 1 
 
        meal_types_label = ttk.Label(self.frame_in_canvas, text="Meal Types:", 
font=self.manage_font.medium_bold_letters_font, background="#333333", 
foreground="#FFFFFF") 
        meal_types_label.grid(row=2, column=2, padx=10, pady=5, sticky="w") 
 
        self.meal_types_var = [] 
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks", "Drinks"] 
        row_num=2 
        for meal_type in meal_types: 
            var = tk.StringVar(value="0")   
            self.meal_types_var.append(var) 
            tickbox = tk.Checkbutton(self.frame_in_canvas, text=meal_type, 
variable=var, font=self.manage_font.medium_bold_letters_font, 
background="#333333", foreground="#00BFFF") 
            tickbox.grid(row=row_num, column=3, padx=10, pady=5, sticky="w") 
            row_num += 1 
 
        get_meal_button = tk.Button(self.frame_in_canvas, text="Get Recommended Meal", font=self.manage_font.medium_bold_heading_font, background="#00BFFF", 
foreground="#FFFFFF", width=70, command=lambda: self.get_meal_recommendation()) 
        get_meal_button.grid(row=row_num, column=3, columnspan=2, rowspan=2, 
padx=10, pady=10) 
 
        self.frame_in_canvas.bind("<Configure>", lambda event, canvas=canvas: 
canvas.configure(scrollregion=canvas.bbox("all"))) 
 
    def get_meal_recommendation(self): 
        user_input = { 
            "Calories": int(self.calories_entry.get()), 
            "Protein": int(self.protein_entry.get()), 
            "Fat": int(self.fat_entry.get()), 
            "Carbohydrates": int(self.carbohydrates_entry.get()), 
            "Ingredients": self.ingredients_entry.get(), 
            "CookingTime": int(self.cooking_time_entry.get()), 
            "NutritionalGoals": self.nutritional_goals_combo.get(), 
            "Budget": int(self.budget_entry.get()), 
            "DietaryRestrictions": self.dietary_restrictions_entry.get(), 
            "Allergies": self.allergies_entry.get(), 
            "MealSize": self.meal_size_entry.get() 
        } 
 
        error_string = [] 
 
        error_item_num=0 
 
        for field, value in user_input.items(): 
            if not value: 
                error_item_num += 1 
                error_string.append(f"\u26A0 Error: Please enter {field}.") 
 
        meal_types = [meal_type for meal_type, value in [("Breakfast", self.meal_types_var[0]), ("Lunch", self.meal_types_var[1]), 
                                                         ("Dinner", self.meal_types_var[2]), ("Snacks", self.meal_types_var[3]), ("Drinks", 
self.meal_types_var[4])] if value.get() == "1"] 
        user_input["MealType"] = ",".join(meal_types) 
        if not user_input["MealType"]: 
            error_string.append(f"\u26A0 Error: Please enter MealType.") 
 
         
        if error_string: 
            self.destroy_error_messages() 
            self.display_error_messages(error_string) 
            return 
 
        recommendation_algorithm = GymMealRecommendationAlgorithm() 
        recommendation_algorithm.load_data() 
        recommendation_algorithm.preprocess_data() 
        recommended_meal_details = recommendation_algorithm.get_recommendation(user_input) 
 
        if self.meal_recommendation_frame: 
            self.meal_recommendation_frame.destroy() 
 
        self.meal_recommendation_frame = tk.Frame(self.frame_in_canvas, 
background="#FFFFFF") 
        self.meal_recommendation_frame.grid(row=20, column=0, columnspan=2, 
padx=10, pady=5, sticky="w") 
 
        close_button = tk.Button(self.meal_recommendation_frame, text="\u2716", 
background="#D11A17", foreground="#FFFFFF", command=lambda 
frame=self.meal_recommendation_frame: frame.destroy()) 
        close_button.grid(row=0, column=2, sticky=tk.NE) 
         
        meal_types_label = ttk.Label(self.meal_recommendation_frame, 
text="Recommended Meal:", font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF") 
        meal_types_label.grid(row=1, column=0, padx=10, pady=5, sticky="w") 
 
        meal_types_label = ttk.Label(self.meal_recommendation_frame, 
text=recommended_meal_details, font=self.manage_font.medium_bold_letters_font, 
background="#FFFFFF") 
        meal_types_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, 
sticky="w") 
 
    def destroy_error_messages(self): 
        if self.error_frame: 
            self.error_frame.destroy() 
             
    def display_error_messages(self, error_string):       
        self.error_frame = tk.Frame(self.canvas)
        self.error_frame.pack(anchor="center", fill=tk.Y) 
 
        # Display error messages for empty fields 
        message_row = 0 
         
        for message in error_string: 
            message_row += 1 
            error_message_frame = tk.Frame(self.error_frame, 
background="#D11A17") 
            error_message_frame.grid(row=message_row, column=0, sticky=tk.W, 
pady=5)   
             
            error_label = tk.Label(error_message_frame, text=message, 
font=self.manage_font.medium_letters_font, background="#D11A17", 
foreground="#FFFFFF", width=70) 
            error_label.pack(side="left") 
 
            close_button = tk.Button(error_message_frame, text="\u2716", 
background="#D11A17", foreground="#FFFFFF", command=lambda 
frame=error_message_frame: frame.destroy()) 
            close_button.pack(side="right") 
 
 
    def add_item(self, item_name, item_type, item_summary, calories, protein, 
fat, carbohydrates, ingredients, cooking_time, image_path, file_path): 
        try:            
            self.error_string = "" 
 
            if not item_name and not item_type: 
                self.error_string = f"Error: \n\n \u26A0 Please enter the item name and type" 
            elif not item_name: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a valid item name" 
            elif not item_type: 
                self.error_string = f"Error: \n\n \u26A0 Please enter a valid item type" 
 
            if not self.error_string: 
                self.cursor.execute(''' 
                    INSERT INTO CustomMeals (MealName, MealType, Summary, 
Calories, Protein, Fat, Carbohydrates, Ingredients, CookingTime, MemberID, 
ImagePath, FilePath) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', ("(CUSTOM) " + item_name, item_type, item_summary, 
calories, protein, fat, carbohydrates, ingredients, cooking_time, 
self.member_id, image_path, file_path)) 

                self.conn.commit() 
 
                self.success_string = "Success: \n\n \u2705 Your meal had been added successfully!" 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while adding the custom meal: {e}") 
 
        finally: 
            if self.error_string: 
                self.message_handler.invalid_message(self.error_string) 
                return 
 
            if self.success_string: 
                self.message_handler.success_message(self.success_string) 
                return 
 
    def get_meal_schedules_for_date(self, date): 
        try: 
                 
                 
         
                self.cursor.execute(''' 
                    SELECT Meals.MealName 
                    FROM MealSchedule 
                    JOIN Meals ON MealSchedule.MealID = Meals.MealID 
                    WHERE MealSchedule.Date = ? 
                ''', (date,)) 
         
                meal_names = [row[0] for row in self.cursor.fetchall()] 
         
                return meal_names 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
            return [] 
 
    def get_meal_schedule_data(self, date, time, meal_type): 
        try: 
             
             
            self.cursor.execute(''' 
                SELECT MealName 
                FROM ( 
                    SELECT Meals.MealName 
                    FROM MealSchedule
                    JOIN Meals ON MealSchedule.MealID = Meals.MealID 
                    WHERE MealSchedule.Date = ? AND MealSchedule.Time = ?  
                    AND Meals.MealType = ? AND MealSchedule.MemberID = ? 
 
                    UNION 
                     
                    SELECT CustomMeals.MealName 
                    FROM MealSchedule 
                    JOIN CustomMeals ON MealSchedule.CustomMealID = 
CustomMeals.CustomMealID 
                    WHERE MealSchedule.Date = ? AND MealSchedule.Time = ?  
                    AND CustomMeals.MealType = ? AND MealSchedule.MemberID = ? 
                ) 
            ''', (date, time, meal_type, self.member_id, date, time, meal_type, 
self.member_id)) 
 
            rows = self.cursor.fetchall() 
            meal_names = [row[0] for row in rows] 
            return meal_names 
 
        except sqlite3.Error as e: 
            messagebox.showerror("Error", f"An error occurred while accessing the database: {e}") 
            return [] 
 
         
    def select_all_custom_meal(self): 
        rows = self.cursor.fetchall() 
        meal_names = [row[0] for row in rows] 
 
        return meal_names 
 
    def get_meal_schedule_days(self): 
        try: 
            current_date = datetime.datetime.now().strftime("%Y-%m-%d") 
 
            self.cursor.execute(''' 
                SELECT DISTINCT Date 
                FROM MealSchedule 
                WHERE Date >= ? AND MemberID = ? 
                ORDER BY Date 
            ''', (self.selected_date, self.member_id)) 
            rows = self.cursor.fetchall() 
            meal_days = [row[0] for row in rows] 
            return meal_days 
         
        except sqlite3.Error as e: 
            print("An error occurred with the database:", e) 

            return [] 
 
    def select_meals_by_type(self, data): 
        self.cursor.execute(''' 
            SELECT MealName FROM Meals 
            WHERE MealType = ? 
        ''', (data,)) 
        default_meal_rows = self.cursor.fetchall() 
 
        self.cursor.execute(''' 
            SELECT MealName FROM CustomMeals 
            WHERE MealType = ? 
        ''', (data,)) 
        custom_meal_rows = self.cursor.fetchall() 
 
        default_meal_names = [row[0] for row in default_meal_rows] 
        custom_meal_names = [row[0] for row in custom_meal_rows] 
 
        meal_names = default_meal_names + custom_meal_names 
 
        return meal_names 
 
    def select_distinct_nutritional_goals(self): 
        self.cursor.execute(''' 
            SELECT DISTINCT NutritionalGoals 
            FROM ( 
                SELECT NutritionalGoals FROM Meals 
                UNION 
                SELECT NutritionalGoals FROM CustomMeals WHERE MemberID = ? 
            ); 
        ''', (1,)) 
 
        unique_rows = self.cursor.fetchall() 
        unique_nutritional_goals = [row[0] for row in unique_rows] 
 
        return unique_nutritional_goals 
    
    def destroy_all_frames(self): 
        self.destroy_error_messages() 
         
        if self.add_meal_frame: 
            self.add_meal_frame.destroy() 
        if self.add_meal_title: 
            self.add_meal_title.destroy() 
 
        if self.remove_meal_frame: 
            self.remove_meal_frame.destroy() 
        if self.remove_meal_title: 
            self.remove_meal_title.destroy() 
 
        if self.select_meal_frame: 
            self.select_meal_frame.destroy() 
        if self.select_meal_title: 
            self.select_meal_title.destroy() 
             
        if self.custom_meal_frame: 
            self.custom_meal_frame.destroy() 
 
        if self.personalised_meal_frame: 
            self.personalised_meal_frame.destroy() 
        if self.personalised_meal_title: 
            self.personalised_meal_title.destroy() 
 
    def check_numeric_input(self, string, length): 
        return (string.isdigit() or string=="") and len(string) <= int(length) 
 
    def upload_image(self, event): 
        image_path = filedialog.askopenfilename(filetypes=[("Image files", 
"*.png *.jpg *.jpeg")]) 
 
        if image_path: 
            image = Image.open(image_path) 
            image = image.resize((200, 200), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image=image) 
 
            self.image_label.config(image=photo, width=100, height=200) 
            self.image_label.image = photo 
            self.image_path = image_path 
 
    def upload_file(self, event): 
        pass 
             
if __name__ == "__main__": 
    app = GymPersonalisedMealPlanner(1, None, None, None, None, None, None, 
None, None).mainloop() 
