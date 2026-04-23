from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)

# In-memory database
members = {}
workouts = {}

# ------------------ UI ROUTE ------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------ MEMBER APIs ------------------

@app.route("/api/members", methods=["GET"])
def get_members():
    return jsonify(list(members.values()))

@app.route("/api/members/<member_id>", methods=["GET"])
def get_member(member_id):
    member = members.get(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member)

@app.route("/api/members", methods=["POST"])
def add_member():
    data = request.get_json()
    member_id = str(uuid.uuid4())

    member = {
        "id": member_id,
        "name": data.get("name"),
        "age": data.get("age"),
        "plan": data.get("plan"),
        "workouts": []
    }

    members[member_id] = member
    return jsonify(member), 201

@app.route("/api/members/<member_id>", methods=["PUT"])
def update_member(member_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404

    data = request.get_json()
    members[member_id].update(data)

    return jsonify(members[member_id])

@app.route("/api/members/<member_id>", methods=["DELETE"])
def delete_member(member_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404

    del members[member_id]
    return jsonify({"message": "Member deleted"})

# ------------------ WORKOUT APIs ------------------

@app.route("/api/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    workout_id = str(uuid.uuid4())

    workout = {
        "id": workout_id,
        "title": data.get("title"),
        "difficulty": data.get("difficulty")
    }

    workouts[workout_id] = workout
    return jsonify(workout), 201

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    return jsonify(list(workouts.values()))

# ------------------ ASSIGN WORKOUT ------------------

@app.route("/api/members/<member_id>/assign/<workout_id>", methods=["POST"])
def assign_workout(member_id, workout_id):
    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404

    if workout_id not in workouts:
        return jsonify({"error": "Workout not found"}), 404

    members[member_id]["workouts"].append(workouts[workout_id])
    return jsonify({"message": "Workout assigned"})

# ------------------ SEARCH ------------------

@app.route("/api/members/search", methods=["GET"])
def search_members():
    name = request.args.get("name", "").lower()

    result = [
        m for m in members.values()
        if name in m["name"].lower()
    ]

    return jsonify(result)

# ------------------ HEALTH CHECK ------------------

@app.route("/api/health")
def health():
    return {"status": "ok"}

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)