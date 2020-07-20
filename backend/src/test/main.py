from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

app = Flask(__name__)



@app.route('/',methods=['GET'])
def home():
    return "hello world"


if __name__ == "__main__":
    app.run(debug=True)