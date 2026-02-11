import tkinter as tk
import random
import string
from gym_font import ManageFont

class GymCaptchaVerification(tk.Toplevel):
    def __init__(self, parent, on_success_callback=None):
        super().__init__(parent)
        self.title("Captcha Verification")
        self.geometry("400x250")
        self.configure(bg="#f2f2f2")
        self.manage_font = ManageFont()
        self.on_success_callback = on_success_callback

        heading_label = tk.Label(self, text="Captcha Verification",
                                 font=self.manage_font.heading_font,
                                 bg="#f2f2f2", fg="#333333")
        heading_label.pack(pady=(20, 10))

        self.captcha_code = self.generate_captcha_code()

        captcha_label = tk.Label(self, text=f"Enter the code: {self.captcha_code}",
                                 font=self.manage_font.medium_bold_heading_font,
                                 bg="#f2f2f2", fg="#C62E46")
        captcha_label.pack(pady=10)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.entry_var,
                         font=self.manage_font.medium_letters_font,
                         width=20)
        entry.pack(pady=10)

        verify_button = tk.Button(self, text="Verify",
                                  font=self.manage_font.medium_bold_heading_font,
                                  bg="#C62E46", fg="white", width=15,
                                  command=self.verify_captcha)
        verify_button.pack(pady=10)

        self.status_label = tk.Label(self, text="", bg="#f2f2f2",
                                     font=self.manage_font.smaller_letters_font,
                                     fg="green")
        self.status_label.pack(pady=10)

    def generate_captcha_code(self, length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def verify_captcha(self):
        user_input = self.entry_var.get().strip()
        if user_input == self.captcha_code:
            self.status_label.config(text="Captcha verified successfully!", fg="green")
            if self.on_success_callback:
                self.on_success_callback()
            self.destroy()
        else:
            self.status_label.config(text="Incorrect code. Please try again.", fg="red")
            self.captcha_code = self.generate_captcha_code()
