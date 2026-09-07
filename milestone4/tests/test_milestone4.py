import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def get_token(client):
    response = client.post(
        "/login",
        json={
            "username": "doctor",
            "password": "doctor123"
        }
    )

    assert response.status_code == 200
    return response.get_json()["token"]


# ============================================================
# UNIT TESTS - ANALYTICS
# ============================================================

def test_analytics(client):

    token = get_token(client)

    response = client.get(
        "/analytics",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "patients" in data
    assert "appointments" in data
    assert "consultations" in data
    assert "prescriptions" in data


def test_patient_analytics(client):

    token = get_token(client)

    response = client.get(
        "/analytics/patients",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total_patients"] >= 0
    assert "gender_distribution" in data
    assert "age_distribution" in data


def test_appointment_analytics(client):

    token = get_token(client)

    response = client.get(
        "/analytics/appointments",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total_appointments"] >= 0
    assert "doctor_distribution" in data
    assert "status_distribution" in data


def test_doctor_analytics(client):

    token = get_token(client)

    response = client.get(
        "/analytics/doctors",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total_doctors"] >= 0
    assert "doctors" in data


# ============================================================
# INTEGRATION TESTS - REPORTS
# ============================================================

def test_patient_report(client):

    token = get_token(client)

    response = client.get(
        "/reports/patients",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["report"] == "Patient Report"
    assert "patients" in data


def test_appointment_report(client):

    token = get_token(client)

    response = client.get(
        "/reports/appointments",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["report"] == "Appointment Report"
    assert "appointments" in data


def test_prescription_report(client):

    token = get_token(client)

    response = client.get(
        "/reports/prescriptions",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["report"] == "Prescription Report"
    assert "prescriptions" in data


def test_summary_report(client):

    token = get_token(client)

    response = client.get(
        "/reports/summary",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["report"] == "MediTrack Summary Report"
    assert "summary" in data


# ============================================================
# CSV EXPORT TESTS
# ============================================================

def test_patient_csv_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/patients/csv",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "patient_id" in response.get_data(as_text=True)


def test_appointment_csv_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/appointments/csv",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "appointment_id" in response.get_data(as_text=True)


def test_prescription_csv_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/prescriptions/csv",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "prescription_id" in response.get_data(as_text=True)


# ============================================================
# PDF EXPORT TESTS
# ============================================================

def test_patient_pdf_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/patients/pdf",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")


def test_appointment_pdf_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/appointments/pdf",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")


def test_prescription_pdf_export(client):

    token = get_token(client)

    response = client.get(
        "/reports/prescriptions/pdf",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")


# ============================================================
# SECURITY TESTS
# ============================================================

def test_analytics_without_token(client):

    response = client.get("/analytics")

    assert response.status_code in [401, 403]


def test_patient_report_without_token(client):

    response = client.get("/reports/patients")

    assert response.status_code in [401, 403]


def test_csv_without_token(client):

    response = client.get("/reports/patients/csv")

    assert response.status_code in [401, 403]


def test_pdf_without_token(client):

    response = client.get("/reports/patients/pdf")

    assert response.status_code in [401, 403]
