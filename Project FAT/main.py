from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/submitquery")
def business1():
    submissionquery = str(request.args.get('query'))
    print(submissionquery)
    return render_template("submission.html")
    
if __name__ == "__main__":
    app.run()
