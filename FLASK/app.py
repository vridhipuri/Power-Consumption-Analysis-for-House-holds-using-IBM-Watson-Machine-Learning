
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
#import os

app=Flask(__name__)
@app.route('/')
def home():
    return render_template("pca.html")

model=pickle.load(open("PCA_model.pkl","rb"))
@app.route('/predict',methods=["POST","GET"])

def predict():
    input_features=[float(x) for x in request.form.values()]
    features_value=[np.array(input_features)]
    
    features_name=['Global_reactive_power', 'Voltage','Global_intensity','Sub_metering_1',
                   'Sub_metering_2','Sub_metering_3']
    df=pd.DataFrame(features_value,columns=features_name)
    output=model.predict(df)[0]
    
    return render_template('result.html', value=output)

if __name__=="__main__":
   # port= int(os.getenv('PORT',8080))
    app.run(debug=False)