from distutils.command.build_scripts import first_line_re
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, Response
from threading import Thread
from web_scrapping import ScrapeData


app = Flask(__name__)

def get_csv():
    with open('dados_legislativo.csv') as file:
        csv = file.read()
    return csv

@app.route("/home", methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        data = request.form.get("filter")
        return redirect(url_for('processing', data=data))
    return render_template('home_page.html')

@app.route("/processing/<data>", methods=["GET"])
def processing(data):
    scrape = ScrapeData(data)
    thr = Thread(target=scrape.execute)
    thr.start()
    thr.join()
    csv = get_csv()
    return Response(
        csv, 
        mimetype="text/csv",
        headers={
            "Content-disposition":
                "attachment; filename=dados_legislativo.csv"        
        }
    )
