import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys
import os

# Append the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from credentials import MY_EMAIL, APP_PASSWORD, RECEIVER_EMAILS, BCC_EMAILS

# Email credentials
sender_email = MY_EMAIL
sender_password = APP_PASSWORD
receiver_emails = RECEIVER_EMAILS
bcc_emails = BCC_EMAILS

# Email content
subject = "Hello the coof"
body = "This email was sent from a Python script!"

# Setting up the MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", ".join(receiver_emails)  # Join all 'to' email addresses
message["Bcc"] = ", ".join(bcc_emails)  # Join all 'bcc' email addresses
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Sending the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_emails + bcc_emails, message.as_string())
    print("Email sent successfully")
except Exception as e:
    print(f"Error sending email: {e}")
