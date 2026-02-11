import tkinter as tk 
import pyglet 
from tkinter import ttk 
from tkinter import Toplevel 
from PIL import Image, ImageTk, ImageDraw, ImageFont 
from gym_font import ManageFont 
from gym_footer import GymFooter 
from gym_header import * 
from gym_function_bank import * 
import sqlite3 
import math 
 
class GymHomePage(tk.Tk): 
    def __init__(self, select_your_gym_callback, gym_features_callback): 
        super().__init__() 
 
        self.ui_manager = UiManager(self, select_your_gym_callback, 
gym_features_callback) 
        self.ui_manager.create_ui() 
 
        self.gym_location_index = None 
         
        style = ttk.Style() 
        style.configure('TButton', background='#FFD700', foreground='#333333', 
font=(12, 'bold')) 
        style.configure('TFrame', background='#333333', foreground='#FFFFFF') 
        style.configure('TLabel', background='#333333', foreground='#FFFFFF', 
font=('Bold', 12)) 
 
    def get_location_id(self): 
        self.gym_location_index = self.ui_manager.get_location_id()
        return self.gym_location_index 
         
class UiManager: 
    def __init__(self, root, select_your_gym_callback, gym_features_callback): 
        self.root = root 
        self.select_your_gym_callback = select_your_gym_callback 
        self.gym_features_callback = gym_features_callback 
        self.gym_location_id = None 
 
    def create_ui(self): 
        self.create_widgets() 
 
    def create_widgets(self): 
        try: 
            self.create_canvas() 
 
            self.create_call_to_action_buttons() 
            self.add_padding() 
 
            self.create_footer() 
 
            self.on_scroll() 
 
        except Exception as e: 
            print("Error creating widgets:", e) 
 
    def create_canvas(self): 
        self.canvas = tk.Canvas(self.root, bg="#f2f2f2") 
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
 
        self.scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview) 
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.bind("<Configure>", self.on_scroll) 
 
        self.main_frame = tk.Frame(self.canvas, bg="#f2f2f2") 
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw") 
 
    def create_call_to_action_buttons(self): 
        try: 
            self.call_to_action_buttons = CallToActionButtons(self.main_frame, 
self.select_your_gym_callback, self.gym_features_callback) 
            self.call_to_action_buttons.pack(pady=20) 
        except Exception as e: 
            print("Error creating Call to Action Buttons:", e) 
 
    def add_padding(self):
        for _ in range(5): 
            tk.Label(self.main_frame, bg="#f2f2f2").pack() 
 
    def create_footer(self): 
        try: 
            self.footer = GymFooter(self.main_frame) 
            self.footer.pack(fill=tk.X) 
        except Exception as e: 
            print("Error creating Footer:", e) 
 
    def on_scroll(self, *args): 
        self.canvas.configure(scrollregion=self.canvas.bbox("all")) 
 
    def home_button_click(self): 
        print("Home button clicked") 
 
    def menu_button_click(self): 
        print("Menu button clicked") 
 
    def search_button_click(self): 
        print("Search button clicked") 
 
    def get_location_id(self): 
        self.gym_location_id = self.call_to_action_buttons.get_location_id() 
        return self.gym_location_id 
 
class CallToActionButtons(tk.Frame): 
    def __init__(self, parent, select_your_gym_callback, gym_features_callback): 
        super().__init__(parent, bg="#f2f2f2") 
        self.pack(fill=tk.BOTH, expand=True) 
         
        self.parent = parent 
 
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight() 
 
        self.gym_location_id = None 
 
        manage_font = ManageFont() 
 
        self.fetch_gym_details() 
 
        image = Image.open("hero_section.jpg") 
        image = image.resize((1500, 1000)) 
 
        # Find the hero description within the text 
        file_path = 'home_page_description.txt' 
        read_text = ReadText(file_path)
        hero_descriptions = read_text.extract_description('Hero Description:') 
 
        text_overlay = self.overlay_image_with_text(image.width, image.height, 
"MAKE A DIFFERENCE", (0, 0, 0, 255), 20, "TT Norms Pro ExtraLight.otf", 630, 
170) 
        title_overlay = self.overlay_image_with_text(image.width, image.height, 
"Ignite Your Potential.", (200, 0, 0, 255), 80, "Koulen-Regular.ttf", 400, 200) 
        subheading_overlay = self.overlay_image_with_text(image.width, 
image.height, "Become A Success.", (0, 0, 0, 255), 80, "Koulen-Regular.ttf", 
450, 300) 
        desc_overlay = self.overlay_image_with_text(image.width, image.height, 
hero_descriptions, (0, 0, 0, 255), 20, "TT Norms Pro ExtraLight.otf", 250, 450) 
 
        combined_image = Image.alpha_composite(image.convert("RGBA"), 
title_overlay) 
        combined_image = Image.alpha_composite(combined_image, text_overlay) 
        combined_image = Image.alpha_composite(combined_image, 
subheading_overlay) 
        combined_image = Image.alpha_composite(combined_image, desc_overlay) 
 
        combined_photo = ImageTk.PhotoImage(combined_image) 
 
        image_label = tk.Label(self, image=combined_photo, bg="#f2f2f2") 
        image_label.image = combined_photo 
        image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, 
sticky="nsew") 
 
        get_started_button = tk.Button(self, text="Get Started", 
background="#D11A17", foreground="#FFFFFF", 
font=manage_font.medium_letters_font) 
        get_started_button.place(x=700, y=700) 
        get_started_button.bind("<Button-1>", lambda event: 
select_your_gym_callback()) 
 
 
        self.columnconfigure(1, weight=1) 
        self.columnconfigure(2, weight=1) 
        self.columnconfigure(3, weight=1) 
 
        self.create_advantage("Better Health", "Improve your health and fitness with our expert trainers.", 0) 
        self.create_advantage("Better Performance", "Boost your athletic performance and achieve your goals.", 1) 
        self.create_advantage("Better Community", "Join a supportive community of fitness enthusiasts.", 2) 
 
        find_gym_frame = tk.Frame(self, bg="#C62E46", bd=2, relief=tk.GROOVE) 
        find_gym_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew") 
 
        # Sub-frame for search elements 
        search_frame = tk.Frame(find_gym_frame, bg="#C62E46") 
        search_frame.pack(padx=10, pady=(10, 5), fill=tk.X)  
 
        search_label = tk.Label(search_frame, text="Locate Your Gym:", 
font=manage_font.larger_letters_font, bg="#C62E46", fg="#FFFFFF") 
        search_label.grid(row=1, column=0, padx=5, pady=5, sticky="w") 
 
        search_label = tk.Label(search_frame, text="Find the perfect gym for your fitness journey with our easy-to-use gym locator tool.", 
font=manage_font.medium_letters_font, bg="#C62E46", fg="#FFFFFF") 
        search_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")        
 
        self.search_var = tk.StringVar() 
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
font=manage_font.medium_letters_font, bd=2, width=125, relief=tk.GROOVE) 
        self.search_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew", 
columnspan=2) 
        self.search_entry.bind("<Return>", self.perform_search) 
 
        search_button = tk.Button(search_frame, text="Search", 
background='#FFE4B5', font=manage_font.medium_letters_font, 
command=self.perform_search) 
        search_button.grid(row=3, column=2, padx=5, pady=5, sticky="e") 
 
        # Sub-frame for gym details 
        self.gym_details_frame = tk.Frame(find_gym_frame, bg="white") 
        self.gym_details_frame.pack(fill="x", padx=10, pady=5) 
 
        self.gym_name_label = tk.Label(self.gym_details_frame, text="Gym Name:", 
font=manage_font.smaller_letters_font, bg="white") 
        self.gym_name_label.pack(fill="x", padx=10, pady=5) 
 
        self.gym_address_label = tk.Label(self.gym_details_frame, 
text="Address:", font=manage_font.smaller_letters_font, bg="white") 
        self.gym_address_label.pack(fill="x", padx=10, pady=5) 
 
        self.gym_email_address_label = tk.Label(self.gym_details_frame, 
text="Email Address:", font=manage_font.smaller_letters_font, bg="white") 
        self.gym_email_address_label.pack(fill="x", padx=10, pady=5) 
 
        self.gym_contact_number_label = tk.Label(self.gym_details_frame, 
text="Contact Number:", font=manage_font.smaller_letters_font, bg="white") 
        self.gym_contact_number_label.pack(fill="x", padx=10, pady=5) 
 
        # Results listbox
        self.results_listbox = tk.Listbox(find_gym_frame, bg="white", bd=2, 
relief=tk.GROOVE, selectmode=tk.SINGLE, exportselection=False) 
        self.results_listbox.pack(fill="both", padx=5, pady=10) 
        self.results_listbox.bind("<<ListboxSelect>>", self.on_result_select) 
 
        self.matching_gyms = self.gym_locations 
 
        for gym in self.matching_gyms: 
            self.results_listbox.insert(tk.END, gym[1]) 
 
        view_gym_button = tk.Button(self.gym_details_frame, text="View Gym", 
background="#FFE4B5", font=manage_font.medium_bold_heading_font) 
        view_gym_button.pack(fill="x", padx=10, pady=5) 
        view_gym_button.bind("<Button-1>", lambda event: 
gym_features_callback()) 
 
        # Reason 1: Better Health 
        self.create_reason("hero_section.jpg", "Better Health", "Improve your health and fitness with our expert trainers.", "Learn More", 3, tk.RIGHT) 
 
        # Reason 2: Better Performance 
        self.create_reason("hero_section.jpg", "Better Performance", "Boost your athletic performance and achieve your goals.", "Learn More", 4, tk.LEFT) 
 
        # Reason 3: Better Community 
        self.create_reason("hero_section.jpg", "Better Community", "Join a supportive community of fitness enthusiasts.", "Learn More", 5, tk.RIGHT) 
 
        image = Image.open("hero_section.jpg") 
        image = image.resize((1500, 1000)) 
 
        text_overlay = self.overlay_image_with_text(image.width, image.height, "BE A PART OF A BIGGER STORY.", (0, 0, 0, 255), 20, "TT Norms Pro ExtraLight.otf", 630, 170) 
        title_overlay = self.overlay_image_with_text(image.width, image.height, 
"The Body Squad", (0, 0, 0, 255), 80, "Koulen-Regular.ttf", 520, 220) 
        desc_overlay = self.overlay_image_with_text(image.width, image.height, "Be a part of Fitness Squad to reach unbelievable milestones and be a part of a bigger goal", (0, 0, 0, 255), 20, "TT Norms Pro ExtraLight.otf", 365, 400) 
 
        combined_image = Image.alpha_composite(image.convert("RGBA"), 
title_overlay) 
        combined_image = Image.alpha_composite(combined_image, text_overlay) 
        combined_image = Image.alpha_composite(combined_image, desc_overlay) 
 
        combined_photo = ImageTk.PhotoImage(combined_image) 
 
        image_label = tk.Label(self, image=combined_photo, bg="#f2f2f2")
        image_label.image = combined_photo 
        image_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10, 
sticky="nsew") 
 
        discover_button = tk.Button(self, text="Discover More", 
background="#333333", foreground="#FFFFFF", 
font=manage_font.medium_letters_font) 
        discover_button.grid(row=6, column=1, padx=(160, 10), pady=10) 
         
        # Testimonials Frame 
 
        self.testimonials = self.members_testimonials 
         
        self.current_page = 0 
        self.testimonials_per_page = 3 
         
        # Create the testimonials frame 
        testimonials_frame = tk.Frame(self, bg="white") 
        testimonials_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=10, 
sticky="nsew") 
 
        testimonials_label = tk.Label(testimonials_frame, text="Success Stories From Our Community", font=manage_font.heading_font, bg="white") 
        testimonials_label.pack(fill="x", padx=10, pady=(10, 5)) 
 
        testimonials_description = tk.Label(testimonials_frame, text="Discover inspiring success stories from our gym community! Click on any of the profile pictures \n to read their testimonials and be motivated to achieve your own fitness goals.", font=manage_font.medium_letters_font, bg="white") 
        testimonials_description.pack(fill="x", padx=10, pady=(10, 5)) 
 
        self.testimonials_frame = tk.Frame(testimonials_frame, bg="white") 
        self.testimonials_frame.pack() 
         
        self.pagination_frame = tk.Frame(testimonials_frame, bg="white") 
        self.pagination_frame.pack() 
 
        self.display_testimonials() 
 
        previous_button = tk.Button(self.pagination_frame, text="\u25C0", 
font=("Helvetica", 12), command=self.show_previous_testimonials) 
        previous_button.pack(side="left", padx=10, pady=5) 
             
        next_button = tk.Button(self.pagination_frame, text="\u25B6", 
font=("Helvetica", 12), command=self.show_next_testimonials) 
        next_button.pack(side="right", padx=10, pady=5) 
 
        for i in range(3): 
            read_more_images = ["hero_section.jpg", "hero_section.jpg", 
"hero_section.jpg"] 
             
            image = Image.open(read_more_images[i]) 
            image = image.resize((500, 500)) 
 
            desc_overlay = self.overlay_image_with_text(image.width, 
image.height, hero_descriptions, (0, 0, 0, 255), 20, "TT Norms Pro ExtraLight.otf", 0, 0) 
 
            combined_image = Image.alpha_composite(image.convert("RGBA"), desc_overlay) 
 
            combined_photo = ImageTk.PhotoImage(combined_image) 
 
            image_label = tk.Label(self, image=combined_photo, bg="#f2f2f2") 
            image_label.image = combined_photo 
            image_label.grid(row=8, column=i, padx=10, pady=10, sticky="nsew") 
 
            discover_button = tk.Button(self, text="Read More", 
background="#333333", foreground="#FFFFFF", 
font=manage_font.medium_letters_font) 
            discover_button.grid(row=8, column=i, padx=(0, 10), pady=10, 
sticky="s") 
                
    def display_testimonials(self): 
        manage_font = ManageFont() 
 
        for widget in self.testimonials_frame.winfo_children(): 
            widget.destroy() 
 
        start_idx = self.current_page * self.testimonials_per_page 
        end_idx = start_idx + self.testimonials_per_page 
 
        for row in self.members_testimonials[start_idx:end_idx]: 
            testimonial_text = row[0] 
            image_path = row[1] 
            frame_color = row[2] 
            name_color = row[3] 
            testimonial_color = row[4] 
            testimonial_date = row[5] 
            first_name = row[6] 
            last_name = row[7] 
 
            testimonial_frame = tk.Frame(self.testimonials_frame, bg=frame_color) 
            testimonial_frame.pack(side="left", padx=10, pady=5) 
            try: 
                image = Image.open(image_path) 
                image = image.resize((400, 400), Image.LANCZOS) 
                image = ImageTk.PhotoImage(image) 
                image_label = tk.Label(testimonial_frame, image=image, 
bg=frame_color, cursor="hand2") 
                image_label.image = image 
                image_label.pack() 
                image_label.bind("<Button-1>", lambda event, name=f"{first_name} {last_name}", description=testimonial_text: self.open_testimonial_popup(name, 
description)) 
 
                testimonials_label = tk.Text(testimonial_frame, 
background=frame_color, foreground=testimonial_color, width=60, height=10, 
font=manage_font.small_bold_heading_font, borderwidth=0) 
                testimonials_label.insert("1.0", testimonial_text) 
                testimonials_label.config(state="disabled") 
                testimonials_label.pack() 
 
                name_label = tk.Label(testimonial_frame, text=f"{first_name} {last_name}", font=manage_font.large_italic_heading_font, bg=frame_color, 
fg=name_color) 
                name_label.pack() 
            except Exception as e: 
                print(f"Error loading image for testimonials: {e}") 
 
    def open_testimonial_popup(self, name, description): 
        TestimonialPage(self.members_testimonials, name, description) 
             
    def show_previous_testimonials(self): 
        total_pages = math.ceil(len(self.members_testimonials) / 
self.testimonials_per_page) 
        self.current_page = (self.current_page - 1) % (total_pages) 
        self.display_testimonials() 
        print(total_pages) 
 
    def show_next_testimonials(self): 
        total_pages = math.ceil(len(self.members_testimonials) / 
self.testimonials_per_page) 
        self.current_page = (self.current_page + 1) % (total_pages) 
        self.display_testimonials() 
             
    def create_advantage(self, title_text, content_text, column): 
        manage_font = ManageFont() 
 
        advantage_frame = ttk.Frame(self, style="TFrame") 
        advantage_frame.grid(row=1, column=column, padx=5, pady=5, sticky="w") 
        advantage_label = ttk.Label(advantage_frame, text=title_text, 
background='#333333', foreground='#FFE4B5', 
font=manage_font.larger_bold_letters_font) 
        advantage_label.pack() 
         
        advantage_description_text = content_text 
        advantage_description = tk.Text(advantage_frame, background='#333333', 
foreground='#FFFFFF', font=manage_font.medium_bold_letters_font, borderwidth=0, 
width=40, height=5) 
        advantage_description.insert("1.0", advantage_description_text) 
        advantage_description.config(state="disabled") 
        advantage_description.pack(anchor=tk.W,padx=10,pady=10) 
 
        advantage_more_button = tk.Button(advantage_frame, text="Join Now", 
background='#FFE4B5', font=manage_font.medium_bold_letters_font) 
        advantage_more_button.pack() 
 
    def create_reason(self, image_path, title_text, content_text, button_text, 
row, image_side): 
        manage_font = ManageFont() 
 
        reason_frame = tk.Frame(self, bg="#ECEBE8") 
        reason_frame.grid(row=row, column=0, columnspan=3, padx=20, pady=10, 
sticky="ew") 
 
        try: 
            reason_image = Image.open(image_path) 
            reason_image = reason_image.resize((800, 600)) 
            reason_image = ImageTk.PhotoImage(reason_image) 
            reason_image_label = tk.Label(reason_frame, image=reason_image, 
bg="#ECEBE8") 
            reason_image_label.image = reason_image 
            reason_image_label.pack(side=image_side, padx=10, pady=10) 
        except Exception as e: 
            print("Error loading image:", e) 
 
        title_label = tk.Label(reason_frame, text=title_text, 
font=manage_font.larger_bold_letters_font, bg="#ECEBE8") 
        title_label.pack() 
 
        content_label = tk.Text(reason_frame, background='#ECEBE8', 
font=manage_font.medium_letters_font,width=50,height=27, borderwidth=0) 
        content_label.insert("1.0", content_text) 
        content_label.config(state="disabled") 
        content_label.pack() 
 
        button = tk.Button(reason_frame, text=button_text, font=manage_font.medium_bold_letters_font, fg="white", bg="#333333") 
        button.pack(side=tk.TOP, padx=20, pady=10) 
 
    def fetch_gym_details(self): 
        try: 
            conn = sqlite3.connect('FitZone.db') 
            cursor = conn.cursor() 
 
            cursor.execute(''' 
                SELECT LocationID, LocationName, Address, EmailAddress, 
ContactNumber 
                FROM GymLocations 
                ORDER BY LocationName ASC; 
            ''') 
            self.gym_locations = cursor.fetchall() 
                 
            cursor.execute('''SELECT Testimonials.TestimonialText, 
Testimonials.ImagePath, Testimonials.FrameColor, Testimonials.NameColor, 
                    Testimonials.TestimonialColor, Testimonials.TestimonialDate, 
Members.FirstName, Members.LastName 
                    FROM Testimonials 
                    JOIN Members ON Testimonials.MemberID = Members.MemberID 
                    ORDER BY Testimonials.TestimonialDate DESC; 
            ''') 
            self.members_testimonials = cursor.fetchall() 
 
            conn.close() 
 
        except sqlite3.Error as e: 
            print("Error occurred:", e) 
            return [], [], [], [] 
             
    def overlay_image_with_text(self, width, height, text, text_colour, 
font_size, font_path, text_x, text_y): 
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Transparent background 
        overlay_draw = ImageDraw.Draw(overlay) 
 
        font = ImageFont.truetype(font_path, font_size) 
 
        text_bbox = overlay_draw.textbbox((0, 0), text, font=font) 
 
        overlay_draw.text((text_x, text_y), text, fill=text_colour, font=font) 
        return overlay 
     
    def on_result_select(self, event): 
        selected_index = self.results_listbox.curselection() 
        if selected_index: 
            index = int(selected_index[0]) 
            selected_gym = self.matching_gyms[index] 
 
            self.gym_location_id = selected_gym[0] 
            self.gym_name_label.config(text="Gym Name: " + selected_gym[1]) 
            self.gym_address_label.config(text="Address: " + selected_gym[2]) 
            self.gym_email_address_label.config(text="Email Address: " + 
selected_gym[3]) 
            self.gym_contact_number_label.config(text="Contact Number: " + 
selected_gym[4]) 
        else: 
            self.gym_name_label.config(text="Gym Name:") 
            self.gym_address_label.config(text="Address:") 
            self.gym_email_address_label.config(text="Email Address:") 
            self.gym_contact_number_label.config(text="Contact Number:") 
             
    def perform_search(self, event=None): 
        search_query = self.search_var.get().lower() 
        self.results_listbox.delete(0, tk.END) 
 
        self.matching_gyms = [gym for gym in self.gym_locations if 
any(search_query in value.lower() for value in gym)] 
        for gym in self.matching_gyms: 
            self.results_listbox.insert(tk.END, gym[1]) 
 
    def get_location_id(self): 
        return self.gym_location_id
