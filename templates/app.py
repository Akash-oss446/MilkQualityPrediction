from flask import Flask, render_template, request
import json
import pickle
import numpy as np
import sklearn
import pandas as pd
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

model=pickle.load(open('finalized_model.pkl','rb'))

with open("columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        ph = int(request.form['phvalue'])
        temperature = int(request.form['temp'])
        
        # Get form values for taste, odor, fat, tub, and color
        taste = request.form['taste']
        odor = request.form['odor']
        fat = request.form['fat']
        tub = request.form['tub']
        color = int(request.form['color1'])

        # Convert categorical inputs to numerical values based on conditions
        # Replace these conditions with the actual values from your form
        taste = 0 if taste == 'badt' else 1
        odor = 0 if odor == 'bado' else 1
        fat = 0 if fat == 'low1' else 1
        tub = 0 if tub == 'low2' else 1

        # Create an array to hold the input values
        x = np.zeros(len(__data_columns))
        x[0] = ph
        x[1] = temperature
        x[2] = taste
        x[3] = odor
        x[4] = fat
        x[5] = tub
        x[6] = color

        # Use the model to make predictions
        prediction = model.predict([x])[0]

        # Return predictions based on the model output
        if prediction == 0:
            return render_template('index.html', prediction_neg="Milk Sample is highly adulterated.")
        elif prediction == 1:
            return render_template('index.html', prediction_neg="Milk Sample is lightly adulterated")
        else:
            return render_template('index.html', prediction_pos="Milk Sample is 100% pure")
    else:
        return render_template('index.html')
if __name__=="__main__":
    app.run()