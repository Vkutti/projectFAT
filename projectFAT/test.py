import imaplib
import smtplib


email_user = "khs.hack.club@gmail.com"
email_password = "yvwj gsdd dbpg cdti"  # Replace with App Password






try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Enable encryption
    server.login(email_user, email_password)
    print("SMTP Login successful!")
    server.quit()
except Exception as e:
    print(f"SMTP Login failed: {e}")

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_password)
    print("IMAP Login successful!")
    mail.logout()
except Exception as e:
    print(f"IMAP Login failed: {e}")