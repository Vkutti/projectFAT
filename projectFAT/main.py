from flask import Flask, render_template, url_for, redirect, request, send_from_directory
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
import functools


# Initialize database connection with error handling
try:
    # Try the direct path first
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FAT.db")
    print(f"Attempting to connect to database at: {db_path}")
    
    if os.path.exists(db_path):
        db = SQL(f"sqlite:///{db_path}")
        print("Database connection successful")
    else:
        print(f"Database file not found at {db_path}, trying alternate path")
        # Try alternate path
        db_path = "FAT.db"
        if os.path.exists(db_path):
            db = SQL(f"sqlite:///{db_path}")
            print("Database connection successful (alternate path)")
        else:
            raise FileNotFoundError(f"Database file not found at {db_path}")
except Exception as e:
    print(f"Database connection error: {str(e)}")
    # Still create the db object with a fallback path to avoid syntax errors
    db = SQL("sqlite:///FAT.db")

app = Flask(__name__)

# Configure app for performance
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Disable in production for performance
app.jinja_env.auto_reload = False

# Email credentials - Consider using environment variables for security
email_user = "khs.hack.club@gmail.com"  # Replace with your email
email_password = "yvwj gsdd dbpg cdti"  # Use app password here
imap_server="imap.gmail.com"
port=993

# Caching decorator for expensive operations
def cache_result(ttl=300):  # Cache for 5 minutes by default
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            if key in cache and current_time - cache[key]['time'] < ttl:
                return cache[key]['result']
            result = func(*args, **kwargs)
            cache[key] = {'result': result, 'time': current_time}
            return result
        return wrapper
    return decorator

def check_for_reply(email_user, email_password):
    """
    Check for email replies that contain 'yes' or 'no' and process them accordingly.
    Returns True if any messages were processed, False otherwise.
    """
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

        messages_processed = False
        
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
                                messages_processed = True
                            # Check if the reply contains "no"
                            elif "no" in email_body.lower():
                                global email_date_no
                                email_date_no= msg["Date"]
                                print("Reply contains 'no'. Running additional code...")
                                run_additional_code_no()  # Trigger additional logic
                                messages_processed = True

                        except Exception as e:
                            print(f"Error decoding email: {e}")
        else:
            print("No unread messages found.")

        # Logout from the server
        mail.logout()
        print("Logged out of IMAP server.")
        
        return messages_processed

    except Exception as e:
        print(f"Error checking email: {e}")
        return False


# Additional code to run when 'yes' is detected in the email reply
def run_additional_code_yes():
    print("\nRunning additional code as the user replied 'yes'.")
    Time = parsedate_to_datetime(email_date_yes)
    try:
        print(glblBusinessName, glblOwnername, glblBusinessType, glblBusinessHours, glblBusinessLocation, glblPhoneNumber, glblEmail, "this is printing by the way")
        
        # First database insertion
        db.execute(
            """
            INSERT INTO fat (businessName, ownername, businessType, businessHours, Email, PhoneNumber, businessLocation)
            VALUES (:businessName, :ownername, :businessType, :businessHours, :Email, :PhoneNumber, :businessLocation)
            """,
            businessName=glblBusinessName,
            ownername=glblOwnername,
            businessType=glblBusinessType,
            businessHours=glblBusinessHours,
            Email=glblEmail,
            PhoneNumber=glblPhoneNumber,
            businessLocation=glblBusinessLocation
        )
        print("Adding to the Log Database")
        
        # Second database insertion
        db.execute(
            """
            INSERT INTO BusinessRequestLogs (businessName, Status, Time)
            VALUES (:businessName, :Status, :Time)
            """,
            businessName=glblBusinessName,
            Status="Yes",
            Time=Time
        )
        print("Added to db")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # This will show you the actual error

def run_additional_code_no():
    print("\nRunning additional code as the user replied 'no'.")
    Time = parsedate_to_datetime(email_date_no)
    try:
        print("Adding to the Log Database")
        db.execute(
            """
            INSERT INTO BusinessRequestLogs (businessName, Status, Time)
            VALUES (:businessName, :Status, :Time)
            """,
            businessName=glblBusinessName,
            Status="NO",
            Time=Time
        )
        print("Added to db")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def start_email_checking_thread(email_user, email_password):
    """
    Start a background thread that checks for email replies periodically
    with exponential backoff when no new messages are found
    """
    check_interval = 2  # Start with 2 seconds
    max_interval = 60   # Maximum interval of 60 seconds
    consecutive_empty_checks = 0
    max_consecutive_empty = 5  # After this many empty checks, increase interval
    
    while True:
        try:
            found_messages = check_for_reply(email_user, email_password)
            
            # If no messages were found, consider increasing the check interval
            if not found_messages:
                consecutive_empty_checks += 1
                if consecutive_empty_checks >= max_consecutive_empty:
                    # Increase interval exponentially up to max_interval
                    check_interval = min(check_interval * 1.5, max_interval)
                    consecutive_empty_checks = 0  # Reset counter
            else:
                # Reset interval and counter if messages were found
                check_interval = 2
                consecutive_empty_checks = 0
            
            # Sleep for the current interval
            time.sleep(check_interval)
        except Exception as e:
            print(f"Error in email checking thread: {str(e)}")
            time.sleep(check_interval)

# Error handling decorator
def handle_db_errors(route_function):
    @functools.wraps(route_function)
    def wrapper(*args, **kwargs):
        try:
            return route_function(*args, **kwargs)
        except Exception as e:
            print(f"Error in route {route_function.__name__}: {str(e)}")
            error_message = f"Database error: {str(e)}"
            return render_template("error.html", error=error_message), 500
    return wrapper

@app.route("/")
@handle_db_errors
def main():
    return render_template("index.html")

# start_email_checking_thread(email_user, email_password)

# Add this function to generate HTML email template
def generate_email_html(business_name, business_type, business_hours, business_location, 
                        community, owner_name, email, phone_number, reply_email, subject):
    """Generate an Apple-inspired HTML email template for business submissions."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Business Request</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f7;
            color: #1d1d1f;
            -webkit-font-smoothing: antialiased;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
        }}
        .email-header {{
            background-color: #000000;
            padding: 30px;
            text-align: center;
        }}
        .email-header img {{
            width: 120px;
            height: auto;
        }}
        .fat-logo {{
            font-size: 48px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 2px;
            margin: 0;
            text-transform: uppercase;
        }}
        .email-content {{
            padding: 40px 30px;
        }}
        .email-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1d1d1f;
        }}
        .info-box {{
            background-color: #f5f5f7;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
        }}
        .business-details {{
            margin-bottom: 20px;
        }}
        .detail-row {{
            display: flex;
            margin-bottom: 15px;
        }}
        .detail-label {{
            font-weight: 600;
            width: 140px;
            color: #86868b;
        }}
        .detail-value {{
            flex: 1;
            color: #1d1d1f;
        }}
        .email-footer {{
            background-color: #f5f5f7;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
            color: #86868b;
        }}
        .button {{
            display: inline-block;
            background-color: #0071e3;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 30px;
            border-radius: 980px;
            font-size: 16px;
            font-weight: 400;
            margin: 10px 5px;
            transition: background-color 0.2s ease;
        }}
        .button:hover {{
            background-color: #0077ed;
        }}
        .button-negative {{
            background-color: #ff3b30;
        }}
        .button-negative:hover {{
            background-color: #ff4f45;
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        @media only screen and (max-width: 600px) {{
            .email-content {{
                padding: 30px 20px;
            }}
            .detail-row {{
                flex-direction: column;
            }}
            .detail-label {{
                width: 100%;
                margin-bottom: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1 class="fat-logo">FAT</h1>
        </div>
        <div class="email-content">
            <h1 class="email-title">New Business Request Submission</h1>
            
            <div class="info-box">
                <div class="business-details">
                    <div class="detail-row">
                        <div class="detail-label">Business Name</div>
                        <div class="detail-value">{business_name}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Business Type</div>
                        <div class="detail-value">{business_type}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Location</div>
                        <div class="detail-value">{business_location}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Hours</div>
                        <div class="detail-value">{business_hours}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Community</div>
                        <div class="detail-value">{community}</div>
                    </div>
                </div>
                
                <div class="business-details">
                    <div class="detail-row">
                        <div class="detail-label">Owner Name</div>
                        <div class="detail-value">{owner_name}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Email</div>
                        <div class="detail-value">{email}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Phone</div>
                        <div class="detail-value">{phone_number}</div>
                    </div>
                </div>
            </div>
            
            <p>Please review the business information above and approve or reject the submission.</p>
            
            <div class="button-container">
                <a href="mailto:{reply_email}?subject=Re: {subject}&body=yes" class="button">Approve</a>
                <a href="mailto:{reply_email}?subject=Re: {subject}&body=no" class="button button-negative">Reject</a>
            </div>
        </div>
        
        <div class="email-footer">
            <p>This is an automated email from the For All of Tracy business directory system.</p>
            <p>&copy; 2023 For All of Tracy. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
    return html

@app.route("/businessForm", methods=["GET", "POST"])
@handle_db_errors
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
        glblCommunity= request.form.get("community")
        glblOwnername = request.form.get("ownername")
        glblEmail = request.form.get("email")
        glblPhoneNumber = request.form.get("phoneNumber")
        uploaded_file = request.files.get('business_license')
        print(glblBusinessHours)
        print(glblCommunity)

        # Insert into database
        temp_file_path = os.path.join("temp", uploaded_file.filename)
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists
        uploaded_file.save(temp_file_path)

        subject = "New Business Request"
        
        # Plain text email body
        plain_text = f"""
Business name: {glblBusinessName}
Business location: {glblBusinessLocation}
Business Hours: {glblBusinessHours}
Owner name: {glblOwnername}
Owner/business email: {glblEmail}
Business type: {glblBusinessType}
Phone Number: {glblPhoneNumber}
        """
        
        # Generate HTML email body
        html_content = generate_email_html(
            glblBusinessName, 
            glblBusinessType, 
            glblBusinessHours, 
            glblBusinessLocation,
            glblCommunity, 
            glblOwnername, 
            glblEmail, 
            glblPhoneNumber,
            email_user,
            subject
        )

        # Send the email
        try:
            # Create email content
            message = MIMEMultipart('alternative')
            message["From"] = email_user
            message["To"] = email_user
            message["Subject"] = subject
            
            # Attach both parts - plain text and HTML
            part1 = MIMEText(plain_text, 'plain')
            part2 = MIMEText(html_content, 'html')
            message.attach(part1)
            message.attach(part2)

            # Attach file if available
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
@handle_db_errors
def business1():
    data = str(request.args.get("enter"))

    if not data:
        return render_template("searchResults.html", businesses=[], category="")

    # Fetch business types for validation
    business_types_query = "SELECT DISTINCT businessType FROM fat"
    business_types_result = db.execute(business_types_query)
    business_types = [row["businessType"].upper() for row in business_types_result]

    # Split input data into keywords
    keywords = data.split()

    # Base query
    query = """
        SELECT businessName, ownername, businessHours, Email, PhoneNumber, businessLocation
        FROM fat
        WHERE 1=1
    """

    parameters = {}
    keyword_conditions = []

    # Filter by business type
    if keywords[0].upper() in business_types:
        query += " AND businessType = :businessType"
        parameters["businessType"] = keywords[0].upper()
        keywords = keywords[1:]

    # Add keyword conditions
    for i, keyword in enumerate(keywords):
        param_name = f"keyword{i}"
        keyword_conditions.append(
            f"businessName LIKE :{param_name} OR ownername LIKE :{param_name} OR Community LIKE :{param_name}"
        )
        parameters[param_name] = f"%{keyword}%"

    if keyword_conditions:
        query += " AND (" + " OR ".join(keyword_conditions) + ")"

    results = db.execute(query, **parameters)

    # Fetch business locations
    location_query = "SELECT businessLocation FROM fat"
    locations = db.execute(location_query)

    # Prepare data
    if not results:
        results = [{"businessName": "No businesses were found"}]
    else:
        results = [
            {key: (value if value is not None else "N/A") for key, value in row.items()}
            for row in results
        ]

    return render_template("searchResults.html", businesses=results, category=data.lower(), businessLocation=locations)

@app.route("/aboutus")
@handle_db_errors
def aboutusrequest():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run()
