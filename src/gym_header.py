import tkinter as tk
from PIL import Image, ImageTk
from gym_user_dropdown_menu import GymUserDropdownMenu
from gym_login import GymLogin
from gym_home_page import GymHomePage

class GymHeader(tk.Frame):
    def __init__(self, parent, logo_path="fitzone.png",
                 select_your_gym_callback=None,
                 gym_features_callback=None):
        super().__init__(parent, bg="#333333")
        self.parent = parent
        self.select_your_gym_callback = select_your_gym_callback
        self.gym_features_callback = gym_features_callback
                   
        self.menu_button = tk.Button(self, text="\u2630",
                                     font=("Helvetica", 18),
                                     bg="#333333", fg="white",
                                     bd=0, highlightthickness=0,
                                     command=self.on_menu_click)
        self.menu_button.pack(side="left", padx=20)

        try:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((120, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(self, image=self.logo_photo,
                                       bg="#333333", cursor="hand2")
            self.logo_label.image = self.logo_photo
            self.logo_label.pack(side="top", pady=5)
            self.logo_label.bind("<Button-1>", self.on_logo_click)
        except Exception:
            self.logo_label = tk.Label(self, text="FitZone",
                                       font=("Helvetica", 20, "bold"),
                                       bg="#333333", fg="white", cursor="hand2")
            self.logo_label.pack(side="top", pady=5)
            self.logo_label.bind("<Button-1>", self.on_logo_click)

        # Right: Search, Notifications, Log In
        right_frame = tk.Frame(self, bg="#333333")
        right_frame.pack(side="right", padx=20)

        self.search_button = tk.Button(right_frame, text="\u2315",  # ⌕
                                       font=("Helvetica", 16),
                                       bg="#333333", fg="white",
                                       bd=0, command=self.on_search_click)
        self.search_button.pack(side="left", padx=10)

        self.notifications_button = tk.Button(right_frame, text="\U0001F514",  
                                              font=("Helvetica", 16),
                                              bg="#333333", fg="white",
                                              bd=0, command=self.on_notifications_click)
        self.notifications_button.pack(side="left", padx=10)

        self.login_button = tk.Button(right_frame, text="LOG IN",
                                      font=("Helvetica", 14, "bold"),
                                      bg="#333333", fg="white",
                                      bd=0, command=self.on_login_click)
        self.login_button.pack(side="left", padx=10)

    # Event handlers
    def on_menu_click(self):
        GymUserDropdownMenu(self.parent)

    def on_search_click(self):
        print("Search clicked")

    def on_notifications_click(self):
        print("Notifications clicked")

    def on_login_click(self):
        GymLogin(self.parent)

    def on_logo_click(self, event=None):
        GymHomePage(self.select_your_gym_callback,
                    self.gym_features_callback)
