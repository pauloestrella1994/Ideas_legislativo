from distutils.command.build_scripts import first_line_re
from flask import Flask, render_template, request, redirect, url_for
from web_scrapping import ScrapeData


app = Flask(__name__)

@app.route("/home", methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        data = request.form.get("filter")
        return redirect(url_for('processing', data=data))
    return render_template('home_page.html')

@app.route("/processing/<data>", methods=["GET"])
def processing(data):
    return render_template("processing.html")


app.run(debug=True)
