from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)

# JWT SECRET KEY
SECRET_KEY = "MediTrack-Milestone3-Secret-Key"

# ============================================================
# MEDITRACK - MILESTONE 3
# REST API, JWT LOGIN, ROLE MANAGEMENT,
# NOTIFICATIONS & AUDIT LOG
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
    },
    {
        "patient_id": "P002",
        "name": "Priya",
        "age": 25,
        "gender": "Female",
        "phone": "9876543211"
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
    },
    {
        "appointment_id": "A002",
        "patient_id": "P002",
        "doctor": "Dr. Priya",
        "date": "2026-09-10",
        "time": "11:00 AM",
        "status": "Booked"
    }
]


# -------------------- OTHER DATA --------------------

consultations = [
    {
        "consultation_id": "C001",
        "patient_id": "P002",
        "symptoms": "Fever and headache",
        "diagnosis": "Viral fever",
        "treatment_plan": "Rest and medication"
    }
]

prescriptions = [
    {
        "prescription_id": "PR001",
        "patient_id": "P002",
        "medicine": "Paracetamol",
        "dosage": "500 mg",
        "duration": "5 days"
    }
]

notifications = [
    {
        "type": "Appointment Reminder",
        "patient_id": "P002",
        "message": "Appointment booked with Dr. Priya on 2026-09-10"
    },
    {
        "type": "Prescription Alert",
        "patient_id": "P002",
        "message": "New prescription generated for P002"
    },
    {
        "type": "Follow-up Reminder",
        "patient_id": "P002",
        "message": "Follow-up appointment is due."
    }
]

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
# JWT TOKEN VERIFICATION
# ============================================================

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Token is missing"
            }), 401

        try:

            parts = auth_header.split()

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({
                    "message": "Use Bearer token"
                }), 401

            token = parts[1]

            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded

        except jwt.ExpiredSignatureError:

            return jsonify({
                "message": "Token has expired"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "message": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated


# ============================================================
# ROLE CHECK
# ============================================================

def role_required(*allowed_roles):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            user_role = request.user.get("role")

            if user_role not in allowed_roles:

                return jsonify({
                    "message": "Access denied",
                    "required_roles": list(allowed_roles),
                    "your_role": user_role
                }), 403

            return f(*args, **kwargs)

        return decorated

    return decorator


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
# LOGIN API WITH JWT
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

            token = jwt.encode(
                {
                    "username": username,
                    "role": user["role"],
                    "exp": datetime.utcnow() + timedelta(hours=2)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            create_audit_log(
                username,
                "Successful login"
            )

            return jsonify({
                "message": "Login successful",
                "username": username,
                "role": user["role"],
                "token": token
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
@token_required
def get_patients():

    return jsonify({
        "total_patients": len(patients),
        "patients": patients
    })


# ============================================================
# GET PATIENT BY ID
# ============================================================

@app.route("/patients/<patient_id>", methods=["GET"])
@token_required
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
@token_required
@role_required("doctor", "admin")
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
        request.user["username"],
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
@token_required
@role_required("doctor", "admin")
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
                request.user["username"],
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
@token_required
@role_required("admin")
def delete_patient(patient_id):

    for patient in patients:

        if patient["patient_id"].lower() == patient_id.lower():

            patients.remove(patient)

            create_audit_log(
                request.user["username"],
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
@token_required
def get_appointments():

    return jsonify({
        "total_appointments": len(appointments),
        "appointments": appointments
    })


# ============================================================
# CREATE APPOINTMENT
# ============================================================

@app.route("/appointments", methods=["POST"])
@token_required
@role_required("doctor", "admin")
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

    patient_found = False

    for patient in patients:

        if patient["patient_id"].lower() == data["patient_id"].lower():

            patient_found = True
            break

    if not patient_found:

        return jsonify({
            "message": "Patient not found"
        }), 404

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
        request.user["username"],
        "Appointment created: " + data["appointment_id"]
    )

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment": appointment
    }), 201


# ============================================================
# UPDATE APPOINTMENT
# ============================================================

@app.route("/appointments/<appointment_id>", methods=["PUT"])
@token_required
@role_required("doctor", "admin")
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
                request.user["username"],
                "Appointment updated: " + appointment_id
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
@token_required
@role_required("doctor", "admin")
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
                request.user["username"],
                "Appointment cancelled: " + appointment_id
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
@token_required
@role_required("doctor")
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
        request.user["username"],
        "Consultation created: " + data["consultation_id"]
    )

    return jsonify({
        "message": "Consultation created successfully",
        "consultation": data
    }), 201


# ============================================================
# GET CONSULTATIONS
# ============================================================

@app.route("/consultations", methods=["GET"])
@token_required
def get_consultations():

    return jsonify({
        "total_consultations": len(consultations),
        "consultations": consultations
    })


# ============================================================
# CREATE PRESCRIPTION
# ============================================================

@app.route("/prescriptions", methods=["POST"])
@token_required
@role_required("doctor")
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
        request.user["username"],
        "Prescription generated: " + data["prescription_id"]
    )

    return jsonify({
        "message": "Prescription generated successfully",
        "prescription": data
    }), 201


# ============================================================
# GET PRESCRIPTIONS
# ============================================================

@app.route("/prescriptions", methods=["GET"])
@token_required
def get_prescriptions():

    return jsonify({
        "total_prescriptions": len(prescriptions),
        "prescriptions": prescriptions
    })


# ============================================================
# FOLLOW-UP NOTIFICATION
# ============================================================

@app.route("/notifications/followup", methods=["POST"])
@token_required
@role_required("doctor", "admin")
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
        request.user["username"],
        "Follow-up reminder created"
    )

    return jsonify({
        "message": "Follow-up reminder created successfully"
    }), 201


# ============================================================
# GET NOTIFICATIONS
# ============================================================

@app.route("/notifications", methods=["GET"])
@token_required
def get_notifications():

    return jsonify({
        "total_notifications": len(notifications),
        "notifications": notifications
    })


# ============================================================
# GET AUDIT LOGS
# ============================================================

@app.route("/audit-logs", methods=["GET"])
@token_required
@role_required("admin")
def get_audit_logs():

    return jsonify({
        "total_logs": len(audit_logs),
        "audit_logs": audit_logs
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def dashboard():

    return jsonify({
        "patients": len(patients),
        "appointments": len(appointments),
        "consultations": len(consultations),
        "prescriptions": len(prescriptions),
        "notifications": len(notifications),
        "audit_logs": len(audit_logs)
    })

@app.route("/analytics", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def analytics():

    return jsonify({
        "message": "MediTrack Analytics",
        "patients": len(patients),
        "appointments": len(appointments),
        "consultations": len(consultations),
        "prescriptions": len(prescriptions),
        "notifications": len(notifications),
        "audit_logs": len(audit_logs)
    })


@app.route("/analytics/patients", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def patient_analytics():

    gender_distribution = {}
    age_distribution = {
        "0-17": 0,
        "18-30": 0,
        "31-45": 0,
        "46-60": 0,
        "61+": 0
    }

    for patient in patients:

        gender = patient.get("gender", "Unknown")
        gender_distribution[gender] = (
            gender_distribution.get(gender, 0) + 1
        )

        try:
            age = int(patient.get("age", 0))

            if age <= 17:
                age_distribution["0-17"] += 1
            elif age <= 30:
                age_distribution["18-30"] += 1
            elif age <= 45:
                age_distribution["31-45"] += 1
            elif age <= 60:
                age_distribution["46-60"] += 1
            else:
                age_distribution["61+"] += 1

        except (ValueError, TypeError):
            pass

    return jsonify({
        "message": "Patient Analytics",
        "total_patients": len(patients),
        "gender_distribution": gender_distribution,
        "age_distribution": age_distribution
    })


@app.route("/analytics/appointments", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def appointment_analytics():

    doctor_distribution = {}
    status_distribution = {}

    for appointment in appointments:

        doctor = appointment.get("doctor", "Unknown")

        doctor_distribution[doctor] = (
            doctor_distribution.get(doctor, 0) + 1
        )

        status = appointment.get("status", "Scheduled")

        status_distribution[status] = (
            status_distribution.get(status, 0) + 1
        )

    return jsonify({
        "message": "Appointment Analytics",
        "total_appointments": len(appointments),
        "doctor_distribution": doctor_distribution,
        "status_distribution": status_distribution
    })


@app.route("/analytics/doctors", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def doctor_analytics():

    doctor_appointments = {}

    for appointment in appointments:

        doctor = appointment.get("doctor", "Unknown")

        doctor_appointments[doctor] = (
            doctor_appointments.get(doctor, 0) + 1
        )

    doctor_consultations = {}

    for consultation in consultations:

        doctor = consultation.get("doctor", "Unknown")

        doctor_consultations[doctor] = (
            doctor_consultations.get(doctor, 0) + 1
        )

    all_doctors = set(
        list(doctor_appointments.keys())
        + list(doctor_consultations.keys())
    )

    doctors = {}

    for doctor in all_doctors:

        doctors[doctor] = {
            "appointments": doctor_appointments.get(doctor, 0),
            "consultations": doctor_consultations.get(doctor, 0)
        }

    return jsonify({
        "message": "Doctor Analytics",
        "total_doctors": len(doctors),
        "doctors": doctors
    })
# ============================================================
# MILESTONE 4 - REPORTS
# ============================================================

@app.route("/reports/patients", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def patient_report():

    return jsonify({
        "report": "Patient Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_patients": len(patients),
        "patients": patients
    })


@app.route("/reports/appointments", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def appointment_report():

    return jsonify({
        "report": "Appointment Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_appointments": len(appointments),
        "appointments": appointments
    })


@app.route("/reports/prescriptions", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def prescription_report():

    return jsonify({
        "report": "Prescription Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_prescriptions": len(prescriptions),
        "prescriptions": prescriptions
    })


@app.route("/reports/summary", methods=["GET"])
@token_required
@role_required("doctor", "admin")
def summary_report():

    return jsonify({
        "report": "MediTrack Summary Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "patients": len(patients),
            "appointments": len(appointments),
            "consultations": len(consultations),
            "prescriptions": len(prescriptions),
            "notifications": len(notifications),
            "audit_logs": len(audit_logs)
        }
    })
# ============================================================
# RUN APPLICATION
# ============================================================
# ============================================================
# MILESTONE 4 - ANALYTICS
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("              MEDITRACK - MILESTONE 3")
    print("       REST API, JWT & NOTIFICATION MANAGEMENT")
    print("=" * 60)

    print("\nServer running at:")
    print("http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )