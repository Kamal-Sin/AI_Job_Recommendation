from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "flask_recommendation_helper"})


@app.route("/explain-score", methods=["POST"])
def explain_score():
    data = request.get_json(force=True) or {}
    score = data.get("score")
    skills = data.get("skills", [])
    job_title = data.get("job_title", "the job")

    if score is None:
        return jsonify({"error": "score is required"}), 400

    explanation = (
        f"This recommendation score ({score}) indicates how well your skills "
        f"{skills} match the requirements for {job_title}."
    )
    return jsonify({"explanation": explanation})


if __name__ == "__main__":
    app.run(debug=True)


