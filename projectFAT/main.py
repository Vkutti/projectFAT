from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from cs50 import SQL



# Create a new database or connect to an existing one
db = SQL("sqlite://FAT.db")


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/enterinfo")
def business1():
    data = str(request.args.get("enter"))
    if data.lower() == "daycare":
        print(data)
        idnumber = 11111
        b_name = db.execute(f"SELECT `BusinessName` FROM FAT WHERE ID = {idnumber}")
        selected_business = str(b_name[0]['BusinessName'])  
        print(selected_business) 
    
    if data.lower() == "catering":
        print(data)
        idnumber = 11112
        b_name = db.execute(f"SELECT `BusinessName` FROM FAT WHERE ID = {idnumber}")
        selected_business = str(b_name[0]['BusinessName'])
        print(selected_business)
        
    return render_template("business1.html", selected_business=selected_business)
    
if __name__ == "__main__":
    app.run()




    