from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# File paths
DOCTORS_FILE = "data/doctors.json"
PATIENTS_FILE = "data/patients.json"
APPOINTMENTS_FILE = "data/appointments.json"

# Load JSON data
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_type = request.form["user_type"]

        users = load_data(DOCTORS_FILE if user_type == "doctor" else PATIENTS_FILE)

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                session["user_type"] = user_type
                return redirect(url_for("dashboard"))

        return "Invalid credentials, try again!"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=session["user"], user_type=session["user_type"])

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if "user" not in session:
        return redirect(url_for("login"))

    appointments = load_data(APPOINTMENTS_FILE)

    if request.method == "POST":
        doctor = request.form["doctor"]
        patient = session["user"]
        time = request.form["time"]

        new_appointment = {"doctor": doctor, "patient": patient, "time": time}
        appointments.append(new_appointment)
        save_data(APPOINTMENTS_FILE, appointments)

    return render_template("appointments.html", appointments=appointments, user=session["user"], user_type=session["user_type"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
