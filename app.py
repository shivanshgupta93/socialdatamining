import os
from flask import Flask, render_template
from routes import facebook_api, twitter_api, api
from consts import SECRET_KEY
###from clock import job_trigger

###job_trigger()

app = Flask(__name__, template_folder='static')

app.register_blueprint(facebook_api)
app.register_blueprint(twitter_api)
app.register_blueprint(api)
app.secret_key = SECRET_KEY

@app.route("/")

def home():
    return render_template("index.html") ###opening index.html on load of application

if __name__ == '__main__':
    app.run()
