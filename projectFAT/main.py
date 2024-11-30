from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from cs50 import SQL
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# db = SQL("sqlite:////absolute/path/to/FAT.db")

# Create a new database or connect to an existing one


app = Flask(__name__)


db = SQL("sqlite:///FAT.db")

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/businessForm", methods=["GET", "POST"])

def form():
    sender_email = "khs.hack.club@gmail.com"  # Replace with your email
    receiver_email = "khs.hack.club@gmail.com"  # Replace with recipient's email
    password = "yvwj gsdd dbpg cdti"
    smtp_server="smtp.gmail.com"
    port=587
    if request.method == "POST":
        businessName = request.form.get("businessName")
        businessLocation = request.form.get("businessLocation")
        businessType = request.form.get("businessType")
        businessHours = request.form.get("businessHours")
        ownername = request.form.get("ownername")
        email = request.form.get("email")
        phoneNumber = request.form.get("phoneNumber")


        # Insert into database



        subject = "New Business Request"
        body = f"""Business name: {businessName}
                 Business location: {businessLocation}
                 Business Hours: {businessHours}
                 Owner name: {ownername}
                 Owner/business email: {email}
                 Business type: {businessType}
                 Phone Number: {phoneNumber}
                         """

        # Set up the MIME
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        try:
            # Create email content
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            # Connect to SMTP server
            print("Connecting to the server...")
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()  # Enable encryption
            print("Logging in...")
            server.login(sender_email, password)
            
            # Send the email
            print("Sending email...")
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
        except smtplib.SMTPAuthenticationError as e:
            print("Authentication error: Please check your email or password.")
            print(f"Error: {e}")
        except Exception as e:
            print(f"Failed to send email: {e}")

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

    b_name = db.execute(f"SELECT `BusinessName` FROM fat WHERE SPECS = '{str(data.upper())}'")

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
    



    