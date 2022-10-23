from flask import Flask, jsonify, request
import pandas as pd
import joblib

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def make_prediction():
    json = request.get_json()
    try:
        model = joblib.load('model/model.pkl')
        ohe = joblib.load('model/ohe.pkl')
    except FileNotFoundError:
        print("Error: File not found")
        
    df = pd.DataFrame(json, index=[0])
    df_fit = ohe.transform(df)
    y_predict = model.predict(df_fit)
    result = {"predicted_price": y_predict[0]}
    return jsonify(result)    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
