from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route("/home", methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        return redirect(url_for('processing'))
    return render_template('home_page.html')

@app.route("/processing", methods=["GET"])
def processing():
    return render_template("processing.html")


app.run(debug=True)
