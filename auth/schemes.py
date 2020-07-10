from flask import request

def basic_auth():
    print("Basic Auth")
    return request.authorization.username == "james" and request.authorization.password == "pw"

def token_auth():
    print("Token Auth")
    return request.authorization.username == "james" and request.authorization.password == "pw"