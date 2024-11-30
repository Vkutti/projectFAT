from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from cs50 import SQL
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading


# db = SQL("sqlite:////absolute/path/to/FAT.db")

# Create a new database or connect to an existing one


app = Flask(__name__)


db = SQL("sqlite:///FAT.db")
email_user = "khs.hack.club@gmail.com"  # Replace with your email
email_password = "yvwj gsdd dbpg cdti"  # Use app password here
imap_server="imap.gmail.com"
port=993

def check_for_reply(email_user, email_password):
    try:
        # Connect to the IMAP server
        print("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        print("mail connected...")
        mail.login(email_user, email_password)  # Login to the IMAP server
        print("IMAP login successful!")
        
        # Select the inbox
        mail.select("inbox")
        print("Inbox selected.")

        # Search for unread messages
        status, messages = mail.search(None, '(UNSEEN)')
        print(f"Search status: {status}, messages found: {messages}")

        if status == "OK" and messages[0]:  # Check if messages were found
            for msg_id in messages[0].split():
                print(f"Fetching message ID: {msg_id}")
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                
                if status != "OK":
                    print(f"Failed to fetch message {msg_id}")
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        raw_email = response_part[1]
                        print(f"Raw email fetched: {raw_email[:50]}...")  # Debug: show a snippet of the raw email

                        try:
                            # Decode the email
                            msg = email.message_from_bytes(raw_email)
                            email_body = ""

                            if msg.is_multipart():
                                # Handle multipart emails
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        email_body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                # Handle single-part emails
                                email_body = msg.get_payload(decode=True).decode()

                            print(f"Email body: {email_body[:50]}...")  # Debug: show a snippet of the email body

                            # Check if the reply contains "yes"
                            if "yes" in email_body.lower():
                                print("Reply contains 'yes'. Running additional code...")
                                run_additional_code()  # Trigger additional logic

                        except Exception as e:
                            print(f"Error decoding email: {e}")
        else:
            print("No unread messages found.")

        # Logout from the server
        mail.logout()
        print("Logged out of IMAP server.")

    except Exception as e:
        print(f"Error checking email: {e}")


# Additional code to run when 'yes' is detected in the email reply
def run_additional_code():
    print("\nRunning additional code as the user replied 'yes'.")
    try:
        print(glblBusinessName, glblOwnername, glblBusinessType, glblBusinessHours, glblBusinessLocation, "this is printing btw")
        db.execute(
                """
                INSERT INTO fat (businessName, ownername, businessType, businessHours, businessLocation)
                VALUES (:businessName, :ownername, :businessType, :businessHours, :businessLocation)
                """,
                businessName = glblBusinessName,
                ownername= glblOwnername,
                businessType= glblBusinessType,
                businessHours=glblBusinessHours,
                businessLocation= glblBusinessLocation,
                )
        print("added to db")
        
        
    except:
        ("shit didnt work")

def start_email_checking_thread(email_user,email_password):
    while True:
        check_for_reply(email_user, email_password)
        time.sleep(5)  # Wait for 30 seconds before checking again

@app.route("/")
def main():
    return render_template("index.html")

# start_email_checking_thread(email_user, email_password)



@app.route("/businessForm", methods=["GET", "POST"])

def form():
    email_user = "khs.hack.club@gmail.com"  # Replace with your email
    email_password = "yvwj gsdd dbpg cdti"
    smtp_server="smtp.gmail.com"
    port=587
    if request.method == "POST":
        global glblBusinessName 
        global glblBusinessLocation
        global glblBusinessType 
        global glblBusinessHours
        global glblOwnername
        global glblEmail 
        global glblPhoneNumber 
        glblBusinessName = request.form.get("businessName")
        glblBusinessLocation = request.form.get("businessLocation")
        glblBusinessType = request.form.get("businessType")
        glblBusinessHours = request.form.get("businessHours")
        glblOwnername = request.form.get("ownername")
        glblEmail = request.form.get("email")
        glblPhoneNumber = request.form.get("phoneNumber")


        # Insert into database



        subject = "New Business Request"
        body = f"""Business name: {glblBusinessName}
                 Business location: {glblBusinessLocation}
                 Business Hours: {glblBusinessHours}
                 Owner name: {glblOwnername}
                 Owner/business email: {glblEmail}
                 Business type: {glblBusinessType}
                 Phone Number: {glblPhoneNumber}
                         """

        # Set up the MIME
        message = MIMEMultipart()
        message["From"] = email_user
        message["To"] = email_user
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        try:
            # Create email content
            message = MIMEMultipart()
            message["From"] = email_user
            message["To"] = email_user
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            # Connect to SMTP server
            print("Connecting to the server...")
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()  # Enable encryption
            print("Logging in...")
            server.login(email_user, email_password)
            
            # Send the email
            print("Sending email...")
            server.sendmail(email_user, email_user, message.as_string())
            print("Email sent successfully!")
        except smtplib.SMTPAuthenticationError as e:
            print("Authentication error: Please check your email or password.")
            print(f"Error: {e}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            # Properly terminate the SMTP session
            print("Logging out...")
            server.quit()  # Ensure the session is closed
            print("Logged out successfully.")
        threading.Thread(target=start_email_checking_thread, args=("khs.hack.club@gmail.com", "yvwj gsdd dbpg cdti"), daemon=True).start()


        # def check_for_reply(email_user, email_password, imap_server="imap.gmail.com"):
        #     try:
        #         print("Checking for replies...")
        #         # Connect to the IMAP server
        #         mail = imaplib.IMAP4_SSL(imap_server)
        #         mail.login(email_user, email_password)
        #         mail.select("inbox")  # Select the inbox

        #         # Search for unread messages
        #         status, messages = mail.search(None, '(UNSEEN)')  # Only fetch unread emails
        #         if status != "OK":
        #             print("No messages found.")
        #             return None

        #         # Process each unread email
        #         for msg_id in messages[0].split():
        #             status, msg_data = mail.fetch(msg_id, "(RFC822)")  # Fetch the full message
        #             if status != "OK":
        #                 print("Failed to fetch email.")
        #                 continue
                    
        #             for response_part in msg_data:
        #                 if isinstance(response_part, tuple):
        #                     msg = email.message_from_bytes(response_part[1])
        #                     email_subject = msg["subject"]
        #                     email_from = msg["from"]
        #                     print(f"New email from {email_from}: {email_subject}")

        #                     # Extract the email body
        #                     if msg.is_multipart():
        #                         for part in msg.walk():
        #                             if part.get_content_type() == "text/plain":
        #                                 email_body = part.get_payload(decode=True).decode()
        #                                 print(f"Email body: {email_body}")
        #                                 if "yes" in email_body.lower():  # Check for 'yes' in the reply
        #                                     return True
        #                     else:
        #                         email_body = msg.get_payload(decode=True).decode()
        #                         print(f"Email body: {email_body}")
        #                         if "yes" in email_body.lower():  # Check for 'yes' in the reply
        #                             return True

        #         return False  # No 'yes' found in the replies
        #     except Exception as e:
        #         print(f"Error checking email: {e}")
        #         return None

        #     finally:
        #         mail.logout()


        # def another_piece_of_code():
        #     db.execute(
        #     """
        #     INSERT INTO fat (businessName, ownername, businessType, businessHours, businessLocation)
        #     VALUES (:businessName, :ownername, :businessType, :businessHours, :businessLocation)
        #     """,
        #     businessName=businessName,
        #     ownername=ownername,
        #     businessType=businessType,
        #     businessHours=businessHours,
        #     businessLocation=businessLocation,
        #     )
        # print("Waiting for a reply...")
        # while True:
        #     reply = check_for_reply(email_user=sender_email, email_password=password)
        #     if reply:
        #         another_piece_of_code()
        #         break

        
   


        return redirect("/")  # Redirect to the home page after successful submission


    # Render the form for GET requests
    return render_template("businessForm.html")

   
    
    
@app.route("/enterinfo")
def business1():
    data = str(request.args.get("enter"))
    businesses = []

    print(data)

    b_name = db.execute(f"SELECT `BusinessName` FROM fat WHERE businessType = '{str(data.upper())}'")

    vals = int(len(b_name))

    print(b_name)
    print(vals)

    for val in range(vals):
        businesses.append(b_name[val]['BusinessName'])
        # selected_business = b_name[0]['BusinessName'] 
        print(businesses) 

        if businesses == []:
            businesses.append("No business in {} category were found")
        
    # businessnamejson = json.dumps(businesses)
    # print(businessnamejson)



    return render_template("searchResults.html", sb=businesses, category=data.lower(), values=vals)
    
if __name__ == "__main__":
    app.run()
    
    



    