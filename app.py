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
      
        ph = float(request.form['phvalue'])
        temperature =float( request.form['temp'])
        
        # Get form values for taste, odor, fat, tub, and color
        taste = 1 if request.form['taste'] == 'Good' else 0
        odor = 1 if request.form['odor'] == 'Good' else 0
        fat = 1 if request.form['fat1'] == 'High' else 0
        tub = 1 if request.form['tub'] == 'High' else 0
        color = request.form['color1']

        # Convert categorical inputs to numerical values based on conditions
        # Replace these conditions with the actual values from your form
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
        prediction = model.predict([x])
        print(prediction)

        # Return predictions based on the model output
        if prediction == 'low':
            return render_template('index1.html', prediction_neg="Milk Sample is highly adulterated,Milk typically has a mild,more bitter taste and odor. Any distinct or strong off-putting smell or taste, such as sourness, bitterness, or rancidity, could indicate spoilage or adulteration")
        elif prediction == 'medium':
            return render_template('index1.html', prediction_neg="Milk Sample is lightly adulterated")
        elif prediction == 'high':
            return render_template('index1.html', prediction_pos="Milk Sample is 100% pure")
    else:
        return render_template('index.html')
if __name__=="__main__":
    app.run(debug=True)