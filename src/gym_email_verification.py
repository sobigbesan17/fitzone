import smtplib 
import random 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from tkinter import messagebox 
 
class EmailVerification: 
    def __init__(self): 
        self.info_string = "" 
 
    def generate_verification_code(self): 
        return str(random.randint(100000, 999999)) 
 
    def send_verification_email(self, recipient, verification_code, title, 
description): 
        smtp_server = 'smtp.gmail.com' 
        smtp_port = 587 
        sender_email = 'FitZoneBot@gmail.com' 
        sender_password = 'kvvyvsuurpegmxtt' 
 
        try: 
            server = smtplib.SMTP(smtp_server, smtp_port) 
            server.starttls() 
            server.login(sender_email, sender_password) 
 
            subject = title 
            message = f"{description}\n\nYour verification code is: 
{verification_code}" 
 
            msg = MIMEMultipart() 
            msg['From'] = sender_email 
            msg['To'] = recipient 
            msg['Subject'] = subject 
 
            msg.attach(MIMEText(message, 'plain')) 
 
            server.sendmail(sender_email, recipient, msg.as_string()) 
            server.quit() 
 
            self.info_string = "Email Sent: \n\n \u2139 A verification email has 
been sent to your email address. Please \n check your inbox and enter the six
digit code." 
 
        except Exception as e: 
            messagebox.showerror("Error", f"Error: An error occurred while 
sending the verification email: {str(e)}") 
 
    def get_info_string(self): 
        return self.info_string 
 
    def verify_email(self, email, title, description): 
        self.verification_code = self.generate_verification_code() 
        self.send_verification_email(email, self.verification_code, title, 
description) 
        return self.verification_code
