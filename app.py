from flask import Flask, jsonify, request

app = Flask(__name__)

members = []

@app.route("/")
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym API"})

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members)

@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()
    members.append(data)
    return jsonify({"message": "Member added successfully"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)