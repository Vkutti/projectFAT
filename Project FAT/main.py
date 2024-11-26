from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/submitquery")
def business1():
    global submissionquery
    submissionquery = str(request.args.get('query'))
    print(submissionquery)

    if submissionquery == '1':
        return render_template("submission.html")
    elif submissionquery == '2':
        return render_template("hackpgage.html")


    
if __name__ == "__main__":
    app.run()
