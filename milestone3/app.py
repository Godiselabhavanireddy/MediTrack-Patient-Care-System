from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ============================================================
# MEDITRACK - MILESTONE 3
# REST API, LOGIN, ROLE MANAGEMENT, NOTIFICATIONS & AUDIT LOG
# ============================================================

# -------------------- USER DATA --------------------

users = [
    {
        "username": "doctor",
        "password": "doctor123",
        "role": "doctor"
    },
    {
        "username": "patient",
        "password": "patient123",
        "role": "patient"
    },
    {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
]

# -------------------- PATIENT DATA --------------------

patients = [
    {
        "patient_id": "P001",
        "name": "Rahul",
        "age": 22,
        "gender": "Male",
        "phone": "9876543210"
    }
]

# -------------------- APPOINTMENT DATA --------------------

appointments = [
    {
        "appointment_id": "A001",
        "patient_id": "P001",
        "doctor": "Dr. Ravi",
        "date": "2026-09-05",
        "time": "10:00 AM",
        "status": "Booked"
    }
]

# -------------------- OTHER DATA --------------------

consultations = []
prescriptions = []
notifications = []
audit_logs = []


# ============================================================
# AUDIT LOG FUNCTION
# ============================================================

def create_audit_log(username, action):
    audit_logs.append({
        "username": username,
        "action": action,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# ============================================================
# HOME API
# ============================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "MediTrack",
        "milestone": "Milestone 3",
        "status": "REST API is running"
    })


# ============================================================
# LOGIN API
# ============================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
        ):

            create_audit_log(
                username,
                "Successful login"
            )

            return jsonify({
                "message": "Login successful",
                "username": username,
                "role": user["role"]
            })

    create_audit_log(
        username if username else "Unknown",
        "Failed login attempt"
    )

    return jsonify({
        "message": "Invalid username or password"
    }), 401


# ============================================================
# GET ALL PATIENTS
# ============================================================

@app.route("/patients", methods=["GET"])
def get_patients():

    return jsonify({
        "total_patients": len(patients),
        "patients": patients
    })


# ============================================================
# GET PATIENT BY ID
# ============================================================

@app.route("/patients/<patient_id>", methods=["GET"])
def get_patient(patient_id):

    for patient in patients:

        if patient["patient_id"].lower() == patient_id.lower():

            return jsonify(patient)

    return jsonify({
        "message": "Patient not found"
    }), 404


# ============================================================
# ADD PATIENT
# ============================================================

@app.route("/patients", methods=["POST"])
def add_patient():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    required_fields = [
        "patient_id",
        "name",
        "age",
        "gender",
        "phone"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "message": field + " is required"
            }), 400

    # Check duplicate patient ID

    for patient in patients:

        if patient["patient_id"].lower() == data["patient_id"].lower():

            return jsonify({
                "message": "Patient ID already exists"
            }), 409

    patients.append({
        "patient_id": data["patient_id"],
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "phone": data["phone"]
    })

    create_audit_log(
        "System",
        "Patient registered: " + data["patient_id"]
    )

    return jsonify({
        "message": "Patient registered successfully",
        "patient": data
    }), 201


# ============================================================
# UPDATE PATIENT
# ============================================================

@app.route("/patients/<patient_id>", methods=["PUT"])
def update_patient(patient_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    for patient in patients:

        if patient["patient_id"].lower() == patient_id.lower():

            patient["name"] = data.get(
                "name",
                patient["name"]
            )

            patient["age"] = data.get(
                "age",
                patient["age"]
            )

            patient["gender"] = data.get(
                "gender",
                patient["gender"]
            )

            patient["phone"] = data.get(
                "phone",
                patient["phone"]
            )

            create_audit_log(
                "System",
                "Patient updated: " + patient_id
            )

            return jsonify({
                "message": "Patient updated successfully",
                "patient": patient
            })

    return jsonify({
        "message": "Patient not found"
    }), 404


# ============================================================
# DELETE PATIENT
# ============================================================

@app.route("/patients/<patient_id>", methods=["DELETE"])
def delete_patient(patient_id):

    for patient in patients:

        if patient["patient_id"].lower() == patient_id.lower():

            patients.remove(patient)

            create_audit_log(
                "System",
                "Patient deleted: " + patient_id
            )

            return jsonify({
                "message": "Patient deleted successfully"
            })

    return jsonify({
        "message": "Patient not found"
    }), 404


# ============================================================
# GET APPOINTMENTS
# ============================================================

@app.route("/appointments", methods=["GET"])
def get_appointments():

    return jsonify({
        "total_appointments": len(appointments),
        "appointments": appointments
    })


# ============================================================
# CREATE APPOINTMENT
# ============================================================

@app.route("/appointments", methods=["POST"])
def create_appointment():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    required_fields = [
        "appointment_id",
        "patient_id",
        "doctor",
        "date",
        "time"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "message": field + " is required"
            }), 400

    # Check patient

    patient_found = False

    for patient in patients:

        if patient["patient_id"].lower() == data["patient_id"].lower():

            patient_found = True
            break

    if not patient_found:

        return jsonify({
            "message": "Patient not found"
        }), 404

    # Check duplicate appointment

    for appointment in appointments:

        if appointment["appointment_id"] == data["appointment_id"]:

            return jsonify({
                "message": "Appointment ID already exists"
            }), 409

    appointment = {
        "appointment_id": data["appointment_id"],
        "patient_id": data["patient_id"],
        "doctor": data["doctor"],
        "date": data["date"],
        "time": data["time"],
        "status": "Booked"
    }

    appointments.append(appointment)

    notifications.append({
        "type": "Appointment Reminder",
        "patient_id": data["patient_id"],
        "message": (
            "Appointment booked with "
            + data["doctor"]
            + " on "
            + data["date"]
        )
    })

    create_audit_log(
        "System",
        "Appointment created: "
        + data["appointment_id"]
    )

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment": appointment
    }), 201


# ============================================================
# UPDATE APPOINTMENT
# ============================================================

@app.route("/appointments/<appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    for appointment in appointments:

        if appointment["appointment_id"] == appointment_id:

            appointment["doctor"] = data.get(
                "doctor",
                appointment["doctor"]
            )

            appointment["date"] = data.get(
                "date",
                appointment["date"]
            )

            appointment["time"] = data.get(
                "time",
                appointment["time"]
            )

            appointment["status"] = data.get(
                "status",
                appointment["status"]
            )

            create_audit_log(
                "System",
                "Appointment updated: "
                + appointment_id
            )

            return jsonify({
                "message": "Appointment updated successfully",
                "appointment": appointment
            })

    return jsonify({
        "message": "Appointment not found"
    }), 404


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

@app.route("/appointments/<appointment_id>", methods=["DELETE"])
def cancel_appointment(appointment_id):

    for appointment in appointments:

        if appointment["appointment_id"] == appointment_id:

            appointment["status"] = "Cancelled"

            notifications.append({
                "type": "Appointment Alert",
                "patient_id": appointment["patient_id"],
                "message": "Appointment cancelled"
            })

            create_audit_log(
                "System",
                "Appointment cancelled: "
                + appointment_id
            )

            return jsonify({
                "message": "Appointment cancelled successfully"
            })

    return jsonify({
        "message": "Appointment not found"
    }), 404


# ============================================================
# CREATE CONSULTATION
# ============================================================

@app.route("/consultations", methods=["POST"])
def create_consultation():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    required_fields = [
        "consultation_id",
        "patient_id",
        "symptoms",
        "diagnosis",
        "treatment_plan"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "message": field + " is required"
            }), 400

    consultations.append(data)

    create_audit_log(
        "Doctor",
        "Consultation created: "
        + data["consultation_id"]
    )

    return jsonify({
        "message": "Consultation created successfully",
        "consultation": data
    }), 201


# ============================================================
# GET CONSULTATIONS
# ============================================================

@app.route("/consultations", methods=["GET"])
def get_consultations():

    return jsonify({
        "total_consultations": len(consultations),
        "consultations": consultations
    })


# ============================================================
# CREATE PRESCRIPTION
# ============================================================

@app.route("/prescriptions", methods=["POST"])
def create_prescription():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    required_fields = [
        "prescription_id",
        "patient_id",
        "medicine",
        "dosage",
        "duration"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "message": field + " is required"
            }), 400

    prescriptions.append(data)

    notifications.append({
        "type": "Prescription Alert",
        "patient_id": data["patient_id"],
        "message": (
            "New prescription generated for "
            + data["patient_id"]
        )
    })

    create_audit_log(
        "Doctor",
        "Prescription generated: "
        + data["prescription_id"]
    )

    return jsonify({
        "message": "Prescription generated successfully",
        "prescription": data
    }), 201


# ============================================================
# GET PRESCRIPTIONS
# ============================================================

@app.route("/prescriptions", methods=["GET"])
def get_prescriptions():

    return jsonify({
        "total_prescriptions": len(prescriptions),
        "prescriptions": prescriptions
    })


# ============================================================
# FOLLOW-UP NOTIFICATION
# ============================================================

@app.route("/notifications/followup", methods=["POST"])
def followup_notification():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data required"
        }), 400

    if "patient_id" not in data or "message" not in data:

        return jsonify({
            "message": "patient_id and message are required"
        }), 400

    notifications.append({
        "type": "Follow-up Reminder",
        "patient_id": data["patient_id"],
        "message": data["message"]
    })

    create_audit_log(
        "System",
        "Follow-up reminder created"
    )

    return jsonify({
        "message": "Follow-up reminder created successfully"
    }), 201


# ============================================================
# GET NOTIFICATIONS
# ============================================================

@app.route("/notifications", methods=["GET"])
def get_notifications():

    return jsonify({
        "total_notifications": len(notifications),
        "notifications": notifications
    })


# ============================================================
# GET AUDIT LOGS
# ============================================================

@app.route("/audit-logs", methods=["GET"])
def get_audit_logs():

    return jsonify({
        "total_logs": len(audit_logs),
        "audit_logs": audit_logs
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({
        "patients": len(patients),
        "appointments": len(appointments),
        "consultations": len(consultations),
        "prescriptions": len(prescriptions),
        "notifications": len(notifications),
        "audit_logs": len(audit_logs)
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              MEDITRACK - MILESTONE 3")
    print("       REST API & NOTIFICATION MANAGEMENT")
    print("=" * 60)

    print("\nServer running at:")
    print("http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )