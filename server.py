from flask import Flask, jsonify, request
import pandas as pd
import joblib

app = Flask(__name__)


@app.route("/test", methods=['POST'])
def test_connection():
    json = request.get_json()
    return jsonify({"result" : "connected"})


@app.route("/predict", methods=['POST'])
def make_prediction():
    json = request.get_json()
    try:
        model = joblib.load('model/model.pkl')
        ohe = joblib.load('model/ohe.pkl')
    except FileNotFoundError:
        print("Error: File not found")

    try:
        df = pd.DataFrame(json, index=[0])
        df_ohe = pd.DataFrame(ohe.transform(df[['town', 'storey_category']]), columns=ohe.get_feature_names(["town", "storey_category"]))
        # Combine transformed categorical and numeric features
        df = pd.concat([df.drop(columns=['town', 'storey_category']), df_ohe], axis=1)
        y_predict = model.predict(df)
        result = {"predicted_price": y_predict[0]}
    except ValueError as e:
        return jsonify(e)
    
    return jsonify(result)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
