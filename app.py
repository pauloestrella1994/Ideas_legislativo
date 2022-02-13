from flask import Flask, render_template


app = Flask(__name__)

@app.route("/home", methods=["GET",])
def home_page():
    return render_template('home_page.html')


app.run(debug=True)
