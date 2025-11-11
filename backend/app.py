from flask import Flask, request, jsonify
from flask_cors import CORS
from prediction_pipeline import SentimentPipeline

app = Flask(__name__)
CORS(app)

pipeline = SentimentPipeline()

@app.route("/", methods=["GET"])
def home():
    return "Sentiment Analysis API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")
    sentiment = pipeline.prediction(text)  # make sure to use .prediction()
    return jsonify({"sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)
