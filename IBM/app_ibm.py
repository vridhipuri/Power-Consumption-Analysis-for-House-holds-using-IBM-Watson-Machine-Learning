
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
#import pickle
#import os

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "RngbIue_enRT-rhbGo48EB5hmd88P3_H1ILnEBsIfnp2"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)
@app.route('/')
def home():
    return render_template("pca.html")

#model=pickle.load(open("PCA_model.pkl","rb"))
@app.route('/predict',methods=["POST","GET"])

def predict():
    input_features=[float(x) for x in request.form.values()]
    features_value=[np.array(input_features)]
    
    features_name=['Global_reactive_power', 'Voltage','Global_intensity','Sub_metering_1',
                   'Sub_metering_2','Sub_metering_3']
    df=pd.DataFrame(features_value,columns=features_name)
    #output=model.predict(df)[0]
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields":[["f0","f1","f2","f3","f4","f5"]],"values":df}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/85bd17a4-d753-48cd-a4a3-24df84cb1029/predictions?version=2022-05-31', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    print(output)
  
    
    return render_template('result.html', value=output)

if __name__=="__main__":
   # port= int(os.getenv('PORT',8080))
    app.run(debug=False)