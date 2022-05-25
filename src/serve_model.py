"""
Flask API of the SMS Spam detection model model.
"""
#import traceback
from flask import Flask, jsonify, request
from flasgger import Swagger
import yaml
import pickle 
from preprocess.preprocess_data import text_prepare

app = Flask(__name__)
swagger = Swagger(app)

def load_yaml_params():
    # Fetch params from yaml params file
    with open("params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_pickle(path_to_pkl):
    with open(path_to_pkl, 'rb') as fd:
        return pickle.load(fd)

def make_prediction(processed_title) -> "list[str]":
    global MODEL_PATH, MLB_PATH
    model = load_pickle(MODEL_PATH)
    mlb = load_pickle(MLB_PATH)
    prediction = model.predict(processed_title)
    return mlb.inverse_transform(prediction)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether an SMS is Spam.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                sms:
                    type: string
                    example: This is an example of an SMS.
    responses:
      200:
        description: "The result of the classification: list of tags as strings."
    """
    input_data = request.get_json()
    title = input_data.get('title')
    processed_title = text_prepare(title)
    tags = make_prediction(processed_title)
    
    res = {
        "tags": tags,
        "classifier": "decision tree",
        "title": title
    }
    print(res)
    return jsonify(res)

# @app.route('/dumbpredict', methods=['POST'])
# def dumb_predict():
#     """
#     Predict whether a given SMS is Spam or Ham (dumb model: always predicts 'ham').
#     ---
#     consumes:
#       - application/json
#     parameters:
#         - name: input_data
#           in: body
#           description: message to be classified.
#           required: True
#           schema:
#             type: object
#             required: sms
#             properties:
#                 sms:
#                     type: string
#                     example: This is an example of an SMS.
#     responses:
#       200:
#         description: "The result of the classification: list of tags as strings."
#     """
#     input_data = request.get_json()
#     sms = input_data.get('sms')
    
#     return jsonify({
#         "result": "Spam",
#         "classifier": "decision tree",
#         "sms": sms
#     })

if __name__ == '__main__':
    params = load_yaml_params()
    train_params = params['train']
    feature_params = params['featurize']

    MODEL_PATH = train_params["model_out"]
    MLB_PATH = feature_params["mlb_out"]

    app.run(host="0.0.0.0", port=8080, debug=True)