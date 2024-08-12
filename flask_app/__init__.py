from flask import Flask
import secrets

app = Flask(__name__)
secret_key_urlsafe = secrets.token_urlsafe(16)
app.secret_key = secret_key_urlsafe