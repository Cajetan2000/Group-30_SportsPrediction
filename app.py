from flask import Flask,request, url_for, redirect, render_template
import pickle
import pandas as pd
import numpy as np
import joblib


# loaded_model = joblib.load('Random_modl.pkl')
# #loaded_model.predict(Input_Testing)
# loaded_model

loaded_model = pickle.load(open('Random_Forest_model.sav',"rb"))
print("loaded_model: ",loaded_model)



app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("Player.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    
    feature_val=[]
    feature_values=[]
    feature_names =[]
    for x,y in request.form.items():
        if y =="" or y.isalpha():
            return render_template('Player.html',pred='{}'.format(0))

        print(x)
        feature_val.append(int(y))
        feature_names.append(x)
    feature_values.append(feature_val)

    print("FV: ",feature_values)
    
    final=pd.DataFrame(feature_values, columns= feature_names)
    print(feature_names)
    print(final)
    y_pred = loaded_model.predict(final)
    #print("YYY:" ,y_pred)
    #output='{0:.f}'.format(y_pred[0], 2)
    # output=10.1

    
    return render_template('Player.html',pred='The player is valued at:\n {}'.format(y_pred[0]))
    
        



if __name__ == '__main__':
    app.run(debug=True)
