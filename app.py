from flask import Flask, jsonify, request
from fetch_exercises import get_exercises, search_exercises

app = Flask(__name__)

all_exercises = get_exercises()

@app.route("/")
def home():
    return "Kokeile http://127.0.0.1:8000/search?q=biceps"

@app.route("/exercises", methods=["GET"])
def list_exercises():
    #Return all exercises as JSON
    if not all_exercises:
        return jsonify({"error": "Failed to fetch exercises"}), 500
    return jsonify(all_exercises)

@app.route("/search", methods=["GET"])
def search():
    # Search exercises based on a keyword
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = search_exercises(all_exercises, query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8000,debug=True)