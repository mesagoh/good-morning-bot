from os import environ
from flask import Flask

app = Flask(__name__)
app.run(environ.get('PORT'))

# TODO: HEROKU web process failed to bind to $PORT within...