from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

def check_code():
    print("worked")
    