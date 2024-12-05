from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from cs50 import SQL
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parsedate_to_datetime
import time
import threading
from email.mime.base import MIMEBase
import os
from email import encoders


# db = SQL("sqlite:////absolute/path/to/FAT.db")

# Create a new database or connect to an existing one


db = SQL("sqlite:///projectFAT/FAT.db")
app = Flask(__name__)




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
                        print(f"Raw email fetched: {raw_email[:50]}...")  

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

                            print(f"Email body: {email_body[:50]}...") 

                            # Check if the reply contains "yes"
                            if "yes" in email_body.lower():
                                global email_date_yes 
                                email_date_yes= msg["Date"]
                                print("Reply contains 'yes'. Running additional code...")
                                run_additional_code_yes()  # Trigger additional logic
                            # Check if the reply contains "no"
                            elif "no" in email_body.lower():
                                global email_date_no
                                email_date_no= msg["Date"]
                                print("Reply contains 'no'. Running additional code...")
                                run_additional_code_no()  # Trigger additional logic

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
def run_additional_code_yes():
    print("\nRunning additional code as the user replied 'yes'.")
    Time= parsedate_to_datetime(email_date_yes)
    try:
        print(glblBusinessName, glblOwnername, glblBusinessType, glblBusinessHours, glblBusinessLocation, "this is printing by the way")
        db.execute(
                """
                INSERT INTO fat (businessName, ownername, businessType, businessHours, businessLocation, Email, PhoneNumber, Community)
                VALUES (:businessName, :ownername, :businessType, :businessHours, :businessLocation,:Email ,:PhoneNumber, :Community)
                """,
                businessName = glblBusinessName,
                ownername= glblOwnername,
                businessType= glblBusinessType,
                businessHours=glblBusinessHours,
                businessLocation= glblBusinessLocation,
                Email = glblEmail, 
                PhoneNumber = glblPhoneNumber, 
                Community = glblCommunity
                )
        print("adding to the Log Database")
        db.execute(
                """
                INSERT INTO BusinessRequestLogs (businessName, Status, Time)
                VALUES (:businessName, :Status, :Time)
                """,
                businessName = glblBusinessName,
                Status= "Yes",
                Time= Time,

                )
        print("added to db")
        
        
    except:
        ("shit didnt work")
def run_additional_code_no():
    print("\nRunning additional code as the user replied 'no'.")
    Time= parsedate_to_datetime(email_date_no)
    try:
        print( "Adding to the Log Database")

        db.execute(
                """
                INSERT INTO BusinessRequestLogs (businessName, Status, Time)
                VALUES (:businessName, :Status, :Time)
                """,
                businessName = glblBusinessName,
                Status= "NO",
                Time= Time,
 
                )
        print("added to db")
        
        
    except:
        ("failed to add to the Log Database")

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
        global glblCommunity

        glblBusinessName = request.form.get("businessName")
        glblBusinessLocation = request.form.get("businessLocation")
        glblBusinessType = request.form.get("businessType")
        glblBusinessHours = request.form.get("businessHours")
        glblOwnername = request.form.get("ownername")
        glblEmail = request.form.get("email")
        glblPhoneNumber = request.form.get("phoneNumber")
        glblCommunity = request.form.get("community")
        uploaded_file = request.files.get('business_license')
        print(glblBusinessLocation)
        print(glblCommunity)

        # Insert into database
        temp_file_path = os.path.join("temp", uploaded_file.filename)
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists
        uploaded_file.save(temp_file_path)



        subject = "New Business Request"
        body = f"""Business name: {glblBusinessName}
                 Business location: {glblBusinessLocation}
                 Business Hours: {glblBusinessHours}
                 Owner name: {glblOwnername}
                 Owner/business email: {glblEmail}
                 Business type: {glblBusinessType}
                 Phone Number: {glblPhoneNumber}
                 Community: {glblCommunity}
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

            try:
                with open(temp_file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={uploaded_file.filename}",
                    )
                    message.attach(part)
            except Exception as e:
                print(f"Error attaching file: {e}")
            
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

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

   


        return redirect("/")  # Redirect to the home page after successful submission


    # Render the form for GET requests
    return render_template("businessForm.html")


@app.route("/enterinfo")
def business1():
    data = str(request.args.get("enter"))

    if not data:
        return render_template("searchResults.html", businesses=[], category="")

    business_types_query = "SELECT DISTINCT businessType FROM fat"
    business_types_result = db.execute(business_types_query)
    business_types = [row["businessType"].upper() for row in business_types_result]

    keywords = data.split()

    query = """
        SELECT businessName, ownername, businessLocation, businessHours, Email, PhoneNumber, Community
        FROM fat
        WHERE 1=1
    """

    parameters = {}
    keyword_conditions = []

    if keywords[0].upper() in business_types:
        # First keyword is a business type
        query += " AND businessType = :businessType"
        parameters["businessType"] = keywords[0].upper()
        keywords = keywords[1:]  

    # Add conditions for remaining keywords
    for i, keyword in enumerate(keywords):
        param_name = f"keyword{i}"
        keyword_conditions.append(
            f"businessName LIKE :{param_name} OR ownername LIKE :{param_name} OR Community LIKE :{param_name}"
        )
        parameters[param_name] = f"%{keyword}%"


    if keyword_conditions:
        query += " AND (" + " OR ".join(keyword_conditions) + ")"

    results = db.execute(query, **parameters)

    if not results:
        results = [{"businessName": "No businesses were found"}]
    else:
        results = [
            {key: (value if value is not None else "") for key, value in row.items()}
            for row in results
        ]

    return render_template("searchResults.html", businesses=results, category=data.lower())


@app.route("/aboutus")
def aboutusrequest():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run()
    
    



    