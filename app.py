from flask import Flask, jsonify, request, render_template
from fetch_exercises import get_exercises, search_exercises

app = Flask(__name__)

all_exercises = get_exercises()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/exercises", methods=["GET"])
def list_exercises():
    if not all_exercises:
        return jsonify({"error": "Failed to fetch exercises"}), 500
    return jsonify(all_exercises)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return ""

    results = search_exercises(all_exercises, query)
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(port=8000, debug=True)