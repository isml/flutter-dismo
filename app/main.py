
from flask import Flask, jsonify,request
import time

import numpy as np
from stl import mesh
import requests







app = Flask(__name__);
@app.route("/bot", methods=["POST"])
def response():
    query = dict(request.form)['query']
    res = query + " " + "naber brooooo güncelledin mi ? "
    return jsonify({"response" : res})
if __name__=="__main__":
    app.run(host="0.0.0.0",)
