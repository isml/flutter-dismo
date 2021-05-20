
from flask import Flask, jsonify,request
import time

import numpy as np
from stl import mesh
import requests







app = Flask(__name__);
@app.route("/bot", methods=["POST"])
def response():
    url = 'https://firebasestorage.googleapis.com/v0/b/dismo-45c00.appspot.com/o/soner.stl?alt=media&token=e97408ce-0253-46c3-b755-72024bb4a1d2'
    r = requests.get(url, allow_redirects=True)

    open('model1.stl', 'wb').write(r.content)

    c1 = mesh.Mesh.from_file('model1.stl')
    query = dict(request.form)['query']
    res = query + " " + "naber brooooo güncelledin mi ? "
    return jsonify({"response" : res})
if __name__=="__main__":
    app.run(host="0.0.0.0",)
