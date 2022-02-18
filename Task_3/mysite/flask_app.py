"""
module uses flask to
interact with the user
"""

from flask import Flask, request, render_template
import task_3


app = Flask(__name__)

@app.route("/")
def index_function():
    return render_template("index.html")


@app.route("/stage2", methods=["POST"])
def map_interaction():
    if request.method == 'POST':
        name = request.form.get("name")
        task_3.main(name)
        return render_template('Friends_map.html')
