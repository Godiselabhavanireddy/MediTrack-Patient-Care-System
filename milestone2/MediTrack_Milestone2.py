
# ============================================================
# MEDITRACK - MILESTONE 2
# Consultation & Prescription Management
# ============================================================

# -------------------- DATA STORAGE ---------------------------

patients = []
appointments = []
consultations = []
prescriptions = []


# ============================================================
# PATIENT CLASS
# ============================================================

class Patient:

    def __init__(self, pid, name, age, gender, phone):
        self.pid = pid
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone


# ============================================================
# APPOINTMENT CLASS
# ============================================================

class Appointment:

    def __init__(self, pid, doctor, date, time):
        self.pid = pid
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Booked"


# ============================================================
# CONSULTATION CLASS
# ============================================================

class Consultation:

    def __init__(
        self,
        consultation_id,
        pid,
        doctor,
        symptoms,
        observations,
        diagnosis,
        lab_results,
        treatment_plan
    ):
        self.consultation_id = consultation_id
        self.pid = pid
        self.doctor = doctor
        self.symptoms = symptoms
        self.observations = observations
        self.diagnosis = diagnosis
        self.lab_results = lab_results
        self.treatment_plan = treatment_plan


# ============================================================
# PRESCRIPTION CLASS
# ============================================================

class Prescription:

    def __init__(
        self,
        prescription_id,
        pid,
        doctor,
        medicine,
        dosage,
        instructions,
        duration
    ):
        self.prescription_id = prescription_id
        self.pid = pid
        self.doctor = doctor
        self.medicine = medicine
        self.dosage = dosage
        self.instructions = instructions
        self.duration = duration


# ============================================================
# FIND PATIENT
# ============================================================

def find_patient(pid):

    for p in patients:

        # Case-insensitive comparison
        if p.pid.lower() == pid.lower():
            return p

    return None


# ============================================================
# REGISTER PATIENT
# ============================================================

def register():

    print("\n" + "=" * 60)
    print("              PATIENT REGISTRATION")
    print("=" * 60)

    pid = input("Patient ID : ").strip()

    if pid == "":
        print("\nPatient ID cannot be empty!")
        return

    # Check whether patient already exists
    if find_patient(pid):

        print("\nPatient already exists!")
        return

    name = input("Name       : ").strip()
    age = input("Age        : ").strip()
    gender = input("Gender     : ").strip()
    phone = input("Phone      : ").strip()

    patient = Patient(
        pid,
        name,
        age,
        gender,
        phone
    )

    patients.append(patient)

    print("\nPatient Registered Successfully!")


# ============================================================
# VIEW PATIENTS
# ============================================================

def view_patients():

    print("\n" + "=" * 60)
    print("                 PATIENT RECORDS")
    print("=" * 60)

    if len(patients) == 0:

        print("No patients available.")
        return

    for p in patients:

        print("-" * 60)

        print("Patient ID :", p.pid)
        print("Name       :", p.name)
        print("Age        :", p.age)
        print("Gender     :", p.gender)
        print("Phone      :", p.phone)

    print("-" * 60)


# ============================================================
# BOOK APPOINTMENT
# ============================================================

def book():

    print("\n" + "=" * 60)
    print("                 BOOK APPOINTMENT")
    print("=" * 60)

    pid = input("Patient ID : ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found!")
        return

    doctor = input("Doctor     : ").strip()
    date = input("Date       : ").strip()
    time = input("Time       : ").strip()

    # Check whether doctor already has the same slot
    for a in appointments:

        if (
            a.doctor.lower() == doctor.lower()
            and a.date.lower() == date.lower()
            and a.time.lower() == time.lower()
            and a.status == "Booked"
        ):

            print("\nThis appointment slot is already booked!")
            return

    appointment = Appointment(
        patient.pid,
        doctor,
        date,
        time
    )

    appointments.append(appointment)

    print("\nAppointment Booked Successfully!")


# ============================================================
# VIEW APPOINTMENTS
# ============================================================

def view_appointments():

    print("\n" + "=" * 60)
    print("                 APPOINTMENT RECORDS")
    print("=" * 60)

    if len(appointments) == 0:

        print("No appointments available.")
        return

    for a in appointments:

        print("-" * 60)

        print("Patient ID :", a.pid)
        print("Doctor     :", a.doctor)
        print("Date       :", a.date)
        print("Time       :", a.time)
        print("Status     :", a.status)

    print("-" * 60)


# ============================================================
# START CONSULTATION
# ============================================================

def consultation():

    print("\n" + "=" * 60)
    print("                  CONSULTATION")
    print("=" * 60)

    pid = input("Patient ID : ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found!")
        return

    doctor = input("Doctor              : ").strip()
    symptoms = input("Symptoms            : ").strip()
    observations = input("Observations        : ").strip()
    diagnosis = input("Diagnosis           : ").strip()
    lab_results = input("Laboratory Results  : ").strip()
    treatment_plan = input("Treatment Plan      : ").strip()

    # Generate consultation ID
    consultation_id = "C" + str(
        len(consultations) + 1
    ).zfill(3)

    consultation_record = Consultation(
        consultation_id,
        patient.pid,
        doctor,
        symptoms,
        observations,
        diagnosis,
        lab_results,
        treatment_plan
    )

    consultations.append(consultation_record)

    print("\nConsultation Saved Successfully!")
    print("Consultation ID :", consultation_id)


# ============================================================
# VIEW CONSULTATION HISTORY
# ============================================================

def view_consultation():

    print("\n" + "=" * 60)
    print("              CONSULTATION HISTORY")
    print("=" * 60)

    if len(consultations) == 0:

        print("No consultation records available.")
        return

    for c in consultations:

        patient = find_patient(c.pid)

        print("-" * 60)

        print("Consultation ID :", c.consultation_id)

        if patient:
            print("Patient Name    :", patient.name)

        print("Patient ID      :", c.pid)
        print("Doctor          :", c.doctor)
        print("Symptoms        :", c.symptoms)
        print("Observations    :", c.observations)
        print("Diagnosis       :", c.diagnosis)
        print("Lab Results     :", c.lab_results)
        print("Treatment Plan  :", c.treatment_plan)

    print("-" * 60)


# ============================================================
# VIEW ONE PATIENT'S TREATMENT HISTORY
# ============================================================

def treatment_history():

    print("\n" + "=" * 60)
    print("              TREATMENT HISTORY")
    print("=" * 60)

    pid = input("Patient ID : ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found!")
        return

    found = False

    print("\nPatient:", patient.name)

    for c in consultations:

        if c.pid.lower() == patient.pid.lower():

            found = True

            print("-" * 60)

            print("Consultation ID :", c.consultation_id)
            print("Doctor          :", c.doctor)
            print("Symptoms        :", c.symptoms)
            print("Observations    :", c.observations)
            print("Diagnosis       :", c.diagnosis)
            print("Lab Results     :", c.lab_results)
            print("Treatment Plan  :", c.treatment_plan)

    if not found:

        print("\nNo treatment history available.")

    print("-" * 60)


# ============================================================
# GENERATE PRESCRIPTION
# ============================================================

def prescription():

    print("\n" + "=" * 60)
    print("              DIGITAL PRESCRIPTION")
    print("=" * 60)

    pid = input("Patient ID : ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found!")
        return

    doctor = input("Doctor       : ").strip()
    medicine = input("Medicine     : ").strip()
    dosage = input("Dosage       : ").strip()
    instructions = input("Instructions : ").strip()
    duration = input("Duration     : ").strip()

    # Generate prescription ID
    prescription_id = "RX" + str(
        len(prescriptions) + 1
    ).zfill(3)

    prescription_record = Prescription(
        prescription_id,
        patient.pid,
        doctor,
        medicine,
        dosage,
        instructions,
        duration
    )

    prescriptions.append(prescription_record)

    print("\nPrescription Generated Successfully!")
    print("Prescription ID :", prescription_id)


# ============================================================
# VIEW PRESCRIPTION HISTORY
# ============================================================

def view_prescription():

    print("\n" + "=" * 60)
    print("              PRESCRIPTION HISTORY")
    print("=" * 60)

    if len(prescriptions) == 0:

        print("No prescription records available.")
        return

    for p in prescriptions:

        patient = find_patient(p.pid)

        print("-" * 60)

        print("Prescription ID :", p.prescription_id)

        if patient:
            print("Patient Name    :", patient.name)

        print("Patient ID      :", p.pid)
        print("Doctor          :", p.doctor)
        print("Medicine        :", p.medicine)
        print("Dosage          :", p.dosage)
        print("Instructions    :", p.instructions)
        print("Duration        :", p.duration)

    print("-" * 60)


# ============================================================
# PATIENT MODULE
# ============================================================

def patient_menu():

    while True:

        print("\n" + "=" * 60)
        print("                  PATIENT MODULE")
        print("=" * 60)

        print("1. View My Profile")
        print("2. View My Appointments")
        print("3. View My Consultation History")
        print("4. View My Prescriptions")
        print("5. Logout")

        choice = input("\nChoice: ").strip()

        # ----------------------------------------------------
        # PROFILE
        # ----------------------------------------------------

        if choice == "1":

            pid = input("Patient ID : ").strip()

            patient = find_patient(pid)

            if patient:

                print("\n" + "-" * 60)

                print("Patient ID :", patient.pid)
                print("Name       :", patient.name)
                print("Age        :", patient.age)
                print("Gender     :", patient.gender)
                print("Phone      :", patient.phone)

                print("-" * 60)

            else:

                print("\nPatient Not Found!")

        # ----------------------------------------------------
        # APPOINTMENTS
        # ----------------------------------------------------

        elif choice == "2":

            pid = input("Patient ID : ").strip()

            patient = find_patient(pid)

            if patient is None:

                print("\nPatient Not Found!")
                continue

            found = False

            for a in appointments:

                if a.pid.lower() == patient.pid.lower():

                    found = True

                    print("-" * 60)

                    print("Doctor :", a.doctor)
                    print("Date   :", a.date)
                    print("Time   :", a.time)
                    print("Status :", a.status)

            if not found:

                print("\nNo appointments found.")

        # ----------------------------------------------------
        # CONSULTATION HISTORY
        # ----------------------------------------------------

        elif choice == "3":

            treatment_history()

        # ----------------------------------------------------
        # PRESCRIPTION HISTORY
        # ----------------------------------------------------

        elif choice == "4":

            pid = input("Patient ID : ").strip()

            patient = find_patient(pid)

            if patient is None:

                print("\nPatient Not Found!")
                continue

            found = False

            for p in prescriptions:

                if p.pid.lower() == patient.pid.lower():

                    found = True

                    print("-" * 60)

                    print("Prescription ID :", p.prescription_id)
                    print("Doctor          :", p.doctor)
                    print("Medicine        :", p.medicine)
                    print("Dosage          :", p.dosage)
                    print("Instructions    :", p.instructions)
                    print("Duration        :", p.duration)

            if not found:

                print("\nNo prescription history available.")

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        elif choice == "5":

            print("\nPatient Logged Out.")
            break

        else:

            print("\nInvalid Choice!")


# ============================================================
# DOCTOR MODULE
# ============================================================

def doctor_menu():

    while True:

        print("\n" + "=" * 60)
        print("                   DOCTOR MODULE")
        print("=" * 60)

        print("1. View Patients")
        print("2. View Appointments")
        print("3. Start Consultation")
        print("4. View Consultation History")
        print("5. Generate Prescription")
        print("6. View Prescription History")
        print("7. View Treatment History")
        print("8. Logout")

        choice = input("\nChoice: ").strip()

        if choice == "1":

            view_patients()

        elif choice == "2":

            view_appointments()

        elif choice == "3":

            consultation()

        elif choice == "4":

            view_consultation()

        elif choice == "5":

            prescription()

        elif choice == "6":

            view_prescription()

        elif choice == "7":

            treatment_history()

        elif choice == "8":

            print("\nDoctor Logged Out.")
            break

        else:

            print("\nInvalid Choice!")


# ============================================================
# ADMIN MODULE
# ============================================================

def admin_menu():

    while True:

        print("\n" + "=" * 60)
        print("                  ADMIN MODULE")
        print("=" * 60)

        print("1. View Patients")
        print("2. View Appointments")
        print("3. View Consultations")
        print("4. View Prescriptions")
        print("5. View Treatment History")
        print("6. Logout")

        choice = input("\nChoice: ").strip()

        if choice == "1":

            view_patients()

        elif choice == "2":

            view_appointments()

        elif choice == "3":

            view_consultation()

        elif choice == "4":

            view_prescription()

        elif choice == "5":

            treatment_history()

        elif choice == "6":

            print("\nAdministrator Logged Out.")
            break

        else:

            print("\nInvalid Choice!")


# ============================================================
# ROLE BASED ACCESS
# ============================================================

def role_login():

    while True:

        print("\n" + "=" * 60)
        print("                 ROLE BASED ACCESS")
        print("=" * 60)

        print("1. Patient")
        print("2. Doctor")
        print("3. Administrator")
        print("4. Back")

        role = input("\nSelect Role: ").strip()

        # ----------------------------------------------------
        # PATIENT
        # ----------------------------------------------------

        if role == "1":

            patient_menu()

        # ----------------------------------------------------
        # DOCTOR
        # ----------------------------------------------------

        elif role == "2":

            username = input("Doctor Username : ").strip()
            password = input("Doctor Password : ").strip()

            if username == "doctor" and password == "doctor123":

                print("\nDoctor Login Successful.")

                doctor_menu()

            else:

                print("\nInvalid Doctor Login!")

        # ----------------------------------------------------
        # ADMINISTRATOR
        # ----------------------------------------------------

        elif role == "3":

            username = input("Admin Username : ").strip()
            password = input("Admin Password : ").strip()

            if username == "admin" and password == "admin123":

                print("\nAdministrator Login Successful.")

                admin_menu()

            else:

                print("\nInvalid Administrator Login!")

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        elif role == "4":

            break

        else:

            print("\nInvalid Role!")


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    print("\n" + "=" * 60)
    print("                  MEDITRACK DASHBOARD")
    print("=" * 60)

    print("Total Patients       :", len(patients))
    print("Total Appointments   :", len(appointments))
    print("Total Consultations  :", len(consultations))
    print("Total Prescriptions  :", len(prescriptions))

    print("=" * 60)


# ============================================================
# MAIN MENU
# ============================================================

while True:

    print("\n" + "=" * 60)
    print("       MEDITRACK - MILESTONE 2")
    print("    CONSULTATION & PRESCRIPTION MANAGEMENT")
    print("=" * 60)

    print("1. Register Patient")
    print("2. View Patients")
    print("3. Book Appointment")
    print("4. View Appointments")
    print("5. Start Consultation")
    print("6. View Consultation History")
    print("7. Generate Prescription")
    print("8. View Prescriptions")
    print("9. Role Based Login")
    print("10. View Treatment History")
    print("11. Dashboard")
    print("12. Exit")

    choice = input("\nEnter Choice: ").strip()

    if choice == "1":

        register()

    elif choice == "2":

        view_patients()

    elif choice == "3":

        book()

    elif choice == "4":

        view_appointments()

    elif choice == "5":

        consultation()

    elif choice == "6":

        view_consultation()

    elif choice == "7":

        prescription()

    elif choice == "8":

        view_prescription()

    elif choice == "9":

        role_login()

    elif choice == "10":

        treatment_history()

    elif choice == "11":

        dashboard()

    elif choice == "12":

        print("\nThank you for using MediTrack.")
        print("Program Closed Successfully.")

        break

    else:

        print("\nInvalid Choice!")
