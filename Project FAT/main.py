from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/business1")
def business1():
    return render_template("business1.html")
    
if __name__ == "__main__":
    app.run()

#Ayush Was Here
#Venkat Came Back