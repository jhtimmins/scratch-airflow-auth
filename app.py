from flask import Flask
import auth

app = Flask(__name__)

@app.route('/')
@auth.login_required("auth.schemes.token_auth")
def hello_world():
    return 'Hello, World!'

print(hello_world)