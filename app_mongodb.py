import numpy as np
from flask import Flask, request, jsonify, render_template
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import pickle
from time import gmtime, strftime
from datetime import datetime


app = Flask(__name__)


client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.oncosteam_server #Select the database
employee = db.employee #Select the collection name


model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

app.route('/predic',methods=['POST'])



@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

   
    int_features = [float(x) for x in request.form.values()]
    tumor_size = int(int_features[0])
    node_status_of_the_tumor = int(int_features[1])
    Age_of_the_patient = int(int_features[2])
    tumor_grade =  int(int_features[3])
    Anomaly_score =  int_features[4]
    
    final_features = [np.array(int_features)]
  
    prediction = model.predict(final_features)
    

    output = round(prediction[0], 2)
    
    output = int(output)

    employee.insert({ "tumor_size":  tumor_size," node_status_of_the_tumor": node_status_of_the_tumor,"Age_of_the_patient":Age_of_the_patient," tumor_grade": tumor_grade ,"Anomaly_score ":Anomaly_score ,"prediction": output,"Date":datetime.now().strftime('%Y-%m-%d'),"Time":datetime.now().strftime('%H:%M:%S')})
    
    return render_template('index.html', prediction_text='[One Repersent High chance of Cancer Recurrence & Zero Repersent  Low chance of Cancer Recurrence] Your Result  :-- {}'.format(output))





if __name__ == "__main__":
    app.run(debug=True)