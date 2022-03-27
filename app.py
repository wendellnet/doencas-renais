from flask import Flask, request, jsonify, render_template, request
from flask_pymongo import PyMongo
from datetime import datetime
import redis
import numpy as np
import pickle
from flask import app 


app = Flask(__name__)
model = pickle.load(open('maquina_preditiva.pkl', 'rb'))

# Flask Session
# https://pythonhosted.org/Flask-Session/
redis_obj = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/',methods=['GET'])
def Home():
    redis_key = 'visit_number'
    visit_number = 1

    if redis_obj.exists(redis_key):
        visit_number = int(redis_obj.get(redis_key).decode("utf-8")) + 1

    redis_obj.set(redis_key, visit_number)
    
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = np.array([[sg, htn, hemo, dm, al, appet, rc, pc]])
        prediction = model.predict(values)

        return render_template('result.html', prediction=prediction)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)