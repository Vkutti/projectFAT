from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from cs50 import SQL
import json


# db = SQL("sqlite:////absolute/path/to/FAT.db")

# Create a new database or connect to an existing one


app = Flask(__name__)

db = SQL("sqlite:///FAT.db")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/enterinfo")
def return_searches():
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
        vals=1
        businesses.append(f"No businesses in the {data.lower()} category were found")
        print(businesses)

    return render_template("searchResults.html", sb=businesses, category=data.lower(), values=vals)

@app.route("/requestbusinessform")
def requestform():
    return render_template("businessForm.html")

@app.route("/aboutus")
def aboutus():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run()




    