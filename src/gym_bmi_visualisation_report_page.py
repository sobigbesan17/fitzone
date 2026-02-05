import tkinter as tk 
from tkinter import ttk, filedialog 
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from gym_function_bank import * 
from scipy.interpolate import make_interp_spline 
from sklearn.svm import SVR 
from sklearn.model_selection import train_test_split 
from gym_user_dropdown_menu import * 
 
class BMIVisualisationReportPage(tk.Tk): 
    def __init__(self, member_id, fitness_dashboard_callback, 
calculate_bmi_callback, bmi_visualisation_callback, gym_meal_planner_callback, 
gym_workout_planner_callback 
                 , view_class_schedule_callback, gym_class_booking_callback, 
gym_class_clashes_callback): 
        super().__init__() 
        self.title("Fitness Dashboard") 
        self.geometry("1000x600") 
 
        self.message_handler = MessageHandler(self) 
 
        self.manage_font = ManageFont() 
        self.user_dropdown_menu = GymUserDropdownMenu(self, 
fitness_dashboard_callback, calculate_bmi_callback, bmi_visualisation_callback, 
gym_meal_planner_callback, 
                                                      
gym_workout_planner_callback, view_class_schedule_callback, 
gym_class_booking_callback, gym_class_clashes_callback) 
        self.user_dropdown_menu.pack(fill="x") 
         
        self.sample_bmi_data =  [round(value, 2) for value in 
np.random.uniform(18.5, 30, 70).tolist()] 
        self.predicted_bmi_data = [] 
 
        self.create_content() 
 
    def create_content(self): 
        self.main_frame = tk.Frame(self) 
        self.main_frame.pack(fill="both", expand=True) 
         
        self.canvas = tk.Canvas(self.main_frame, background="white") 
        self.canvas.pack(side="left", fill="both", expand=True) 
 
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", 
command=self.canvas.yview) 
        self.scrollbar.pack(side="right", fill="y") 
 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.bind("<Configure>", self.configure_canvas) 
 
        self.bmi_visualisation_frame = tk.Frame(self.canvas, 
background="#FFFFFF") 
        self.canvas.create_window((0, 0), window=self.bmi_visualisation_frame) 
 
        self.create_bmi_visualisation_report_page() 
 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def create_bmi_visualisation_report_page(self): 
        bmi_label = tk.Label(self.bmi_visualisation_frame, text="BMI Visualisation Page", background="#FFFFFF", font=self.manage_font.heading_font) 
        bmi_label.pack(pady=(20, 10)) 
 
        average_bmi = self.calculate_average_bmi(self.sample_bmi_data) 
        min_bmi = np.min(self.sample_bmi_data) 
        median_bmi = np.median(self.sample_bmi_data) 
        max_bmi = np.max(self.sample_bmi_data) 
        bmi_quartile_1 = np.percentile(self.sample_bmi_data, 25) 
        bmi_quartile_3 = np.percentile(self.sample_bmi_data, 75) 
 
        self.bmi_statistics_frame = tk.Frame(self.bmi_visualisation_frame, 
background="#333333") 
        self.bmi_statistics_frame.pack() 
 
        bmi_category = self.calculate_bmi_category(average_bmi) 
         
        average_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"Average 
BMI: {average_bmi:.2f} ({bmi_category})", width=150, background="#333333", 
foreground="#FFFFFF", font=self.manage_font.medium_bold_heading_font) 
        average_bmi_label.pack() 
         
        min_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"Lowest BMI: 
{min_bmi:.2f}", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        min_bmi_label.pack() 
 
        median_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"Median 
BMI: {median_bmi:.2f}", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        median_bmi_label.pack() 
         
        max_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"Highest BMI: 
{max_bmi:.2f}", background="#333333", foreground="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        max_bmi_label.pack() 

        quartile_1_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"25th 
Percentile (Q1): {bmi_quartile_1:.2f}", background="#333333", 
foreground="#FFFFFF", font=self.manage_font.medium_letters_font) 
        quartile_1_bmi_label.pack() 
         
        quartile_3_bmi_label = tk.Label(self.bmi_statistics_frame, text=f"75th 
Percentile (Q3): {bmi_quartile_3:.2f}", background="#333333", 
foreground="#FFFFFF", font=self.manage_font.medium_letters_font) 
        quartile_3_bmi_label.pack() 
 
        self.personalised_bmi_recommendation_button = 
tk.Button(self.bmi_visualisation_frame, text="Personalised BMI Recommendation", 
background="#FFE4B5", font=self.manage_font.medium_letters_font) 
        self.personalised_bmi_recommendation_button.pack(pady=10) 
 
        self.create_bmi_tables() 
 
        self.open_button = tk.Button(self.bmi_visualisation_frame, 
text="\U0001F513 Open BMI Data", background="#1E90FF", 
font=self.manage_font.medium_letters_font, command=self.open_bmi_data) 
        self.open_button.pack() 
 
        self.save_button = tk.Button(self.bmi_visualisation_frame, 
text="\U0001F4BE Save BMI Data", background="#1E90FF", 
font=self.manage_font.medium_letters_font, command=self.save_bmi_data) 
        self.save_button.pack() 
 
        self.num_data_points = tk.IntVar(value=0) 
        self.num_data_points_label = tk.Label(self.bmi_visualisation_frame, 
text="Additional Data Points:", background="#FFFFFF", 
font=self.manage_font.medium_letters_font) 
        self.num_data_points_label.pack() 
        self.num_data_points_menu = tk.OptionMenu(self.bmi_visualisation_frame, 
self.num_data_points, 1, 2, 3, 5, 7) 
        
self.num_data_points_menu.config(font=self.manage_font.medium_letters_font) 
        self.num_data_points_menu.pack() 
 
        self.predict_bmi_button = tk.Button(self.bmi_visualisation_frame, 
text="Predict BMI for Next Days", background="#FFE4B5", 
font=self.manage_font.medium_letters_font, command=self.predict_bmi) 
        self.predict_bmi_button.pack() 
 
        self.predicted_bmi_data = [] 
 
        self.display_bmi_visualization(self.sample_bmi_data) 
 
    def calculate_bmi_category(self, average_bmi):
        if average_bmi < 18.5: 
            return "Underweight" 
        elif 18.5 <= average_bmi < 24.9: 
            return "Normal Weight" 
        elif 24.9 <= average_bmi < 29.9: 
            return "Overweight" 
        elif 30 <= average_bmi < 34.9: 
            return "Obese Class 1" 
        elif 35 <= average_bmi < 39.9: 
            return "Obese Class 2" 
        else: 
            return "Obese Class 3" 
 
 
    def create_bmi_tables(self): 
        tree_style = ttk.Style() 
        tree_style.configure("Treeview", 
font=self.manage_font.medium_letters_font) 
        tree_style.configure("Custom.Treeview.Heading", 
font=self.manage_font.medium_bold_heading_font) 
 
        num_data_points = len(self.sample_bmi_data) 
        num_tables = (num_data_points + 9) // 10  # Calculate the number of 
tables needed 
 
        for table_num in range(num_tables): 
            start_index = table_num * 10 
            end_index = min((table_num + 1) * 10, num_data_points)  # Ensure we 
don't go beyond the data length 
 
            table_frame = tk.Frame(self.bmi_visualisation_frame, 
background="#FFFFFF") 
            table_frame.pack() 
 
            table_data = self.sample_bmi_data[start_index:end_index] 
 
            treeview = ttk.Treeview(table_frame, columns=[str(i) for i in 
range(len(table_data))], show="headings", style="Custom.Treeview", height=2) 
             
            for i in range(len(table_data)): 
                treeview.heading(str(i), text=f"BMI {start_index + i + 1}") 
                treeview.column(str(i), width=100) 
             
            treeview.pack(fill="both", pady=10) 
            treeview.insert("", "end", values=table_data) 
 
    def open_bmi_data(self): 
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) 
        if file_path: 
            try: 
                with open(file_path, "r") as file: 
                    lines = file.readlines() 
                self.sample_bmi_data = [float(value) for line in lines for value 
in line.strip().split('\t')] 
                self.main_frame.destroy() 
                self.create_content() 
            except FileNotFoundError: 
                error_string = "Error: \n\n \u26A0 File not found." 
            except ValueError: 
               error_string = "Error: \n\n \u26A0 Invalid file format." 
            except Exception as e: 
                error_string = f"Error: \n\n \u26A0 {str(e)}" 
            finally: 
                if error_string: 
                    self.message_handler.invalid_message(error_string) 
 
    def save_bmi_data(self): 
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
filetypes=[("Text files", "*.txt")]) 
        if file_path: 
            with open(file_path, "w") as file: 
                file.write("\t".join(map(str, self.sample_bmi_data))) 
 
    def display_bmi_visualization(self, data): 
        self.bmi_visualisation_graph_frame = 
tk.Frame(self.bmi_visualisation_frame, background="#FFFFFF") 
        self.bmi_visualisation_graph_frame.pack(fill='x') 
         
        if data: 
            self.create_combined_graph(self.bmi_visualisation_graph_frame, data) 
 
    def configure_canvas(self, event): 
        self.canvas.config(scrollregion=self.canvas.bbox("all")) 
 
    def calculate_average_bmi(self, data): 
        if data: 
            average_bmi = sum(data) / len(data) 
            return average_bmi 
        else: 
            return 0.0 
 
    def create_combined_graph(self, parent_frame, data): 
        fig = Figure(figsize=(16, 6), dpi=100) 
        ax1 = fig.add_subplot(111)
        x = np.arange(len(data)) 
        y = data 
 
        ax1.bar(x, y, color='green', alpha=0.5, label='BMI Bar Chart Data') 
 
        # Spline Graph 
        x_new = np.linspace(x.min(), x.max(), 300) 
        spl = make_interp_spline(x, y, k=min(len(data) - 1, 3)) 
        y_new = spl(x_new) 
 
        ax1.plot(x_new, y_new, label='Spline Curve', linestyle='-', 
color='skyblue') 
        ax1.scatter(x, y, marker='o', color='skyblue', label='Known Data') 
 
        if self.predicted_bmi_data: 
            ax1.scatter(np.arange(len(data), len(data) + 
len(self.predicted_bmi_data)), 
                        self.predicted_bmi_data, marker='x', color='orange', 
label='Predicted Data') 
            ax1.axvline(x=len(data) - 1, color='red', linestyle='--', 
label='Prediction Start') 
 
        ax1.set_xlabel('Measurement') 
        ax1.set_ylabel('BMI') 
        ax1.set_title('BMI Data Graph') 
 
        ax1.legend(loc='lower right') 
 
        canvas = FigureCanvasTkAgg(fig, master=parent_frame) 
        canvas.get_tk_widget().pack() 
 
    def predict_bmi(self): 
        num_additional_points = self.num_data_points.get() 
        if len(self.sample_bmi_data) < 3: 
            error_string = "Error: \n\n \u26A0 Not enough BMI data points." 
            self.message_handler.invalid_message(error_string) 
            return 
             
        if num_additional_points > 0: 
            self.bmi_visualisation_graph_frame.destroy() 
             
            # Prepare the data for SVR 
            X = np.arange(len(self.sample_bmi_data)).reshape(-1, 1) 
            y = np.array(self.sample_bmi_data) 
 
            # Split the data into training and test sets 
            X_train, X_test, y_train, y_test = train_test_split(X, y, 
test_size=0.2, random_state=42)
 
            # Create and train an SVR model with RBF kernel 
            svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1) 
            svr_rbf.fit(X_train, y_train) 
 
            next_days = np.arange(len(self.sample_bmi_data), 
len(self.sample_bmi_data) + num_additional_points).reshape(-1, 1) 
 
            if len(next_days) > 0: 
                predicted_data = svr_rbf.predict(next_days) 
                self.predicted_bmi_data = predicted_data.tolist() 
 
                # Display the updated visualization 
                self.display_bmi_visualization(self.sample_bmi_data) 
 
if __name__ == "__main__": 
    app = BMIVisualisationReportPage(1, None, None, None, None, None) 
    app.mainloop()
