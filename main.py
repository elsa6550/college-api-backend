from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 8UgJumaxCcm1P9tv8hYl7iIOWct5ozGd45mvglnV  # replace with your real key
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

@app.route("/")
def home():
    return "✅ College Data API is running!"

@app.route("/college", methods=["GET"])
def get_college_data():
    college_name = request.args.get("name")
    if not college_name:
        return jsonify({"error": "Please provide a college name"}), 400

    params = {
        "school.name": college_name,
        "api_key": API_KEY,
        "fields": "school.name,school.city,school.state,latest.admissions.admission_rate.overall,"
                  "latest.admissions.sat_scores.average.overall,"
                  "latest.admissions.act_scores.midpoint.cumulative,"
                  "latest.cost.tuition.out_of_state,latest.cost.tuition.in_state"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return jsonify({"error": "College not found. Try a different name."}), 404

    college = data["results"][0]

    result = {
        "name": college.get("school.name", "N/A"),
        "location": f"{college.get('school.city', '')}, {college.get('school.state', '')}",
        "acceptance_rate": college.get("latest.admissions.admission_rate.overall", "N/A"),
        "avg_sat": college.get("latest.admissions.sat_scores.average.overall", "N/A"),
        "avg_act": college.get("latest.admissions.act_scores.midpoint.cumulative", "N/A"),
        "in_state_tuition": college.get("latest.cost.tuition.in_state", "N/A"),
        "out_of_state_tuition": college.get("latest.cost.tuition.out_of_state", "N/A")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
