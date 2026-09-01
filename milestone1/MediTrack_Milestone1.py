
"""
=============================================================
                    MEDITRACK
        Integrated Patient Care Management System

                       MILESTONE 1

        Patient Registration
        Patient Profile Management
        Appointment Scheduling
        Patient Information Retrieval
        Appointment Slot Management
=============================================================
"""


# ===========================================================
# DATA STORAGE
# ===========================================================

patients = []
appointments = []


# ===========================================================
# PATIENT CLASS
# ===========================================================

class Patient:

    def __init__(
        self,
        pid,
        name,
        age,
        gender,
        phone,
        email,
        address,
        blood_group,
        allergies,
        medical_history
    ):

        self.pid = pid
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.blood_group = blood_group
        self.allergies = allergies
        self.medical_history = medical_history


# ===========================================================
# APPOINTMENT CLASS
# ===========================================================

class Appointment:

    def __init__(
        self,
        appointment_id,
        pid,
        doctor,
        department,
        date,
        time,
        reason
    ):

        self.appointment_id = appointment_id
        self.pid = pid
        self.doctor = doctor
        self.department = department
        self.date = date
        self.time = time
        self.reason = reason
        self.status = "Booked"


# ===========================================================
# UTILITY FUNCTIONS
# ===========================================================

def line():
    print("-" * 65)


def header(title):

    print("\n")
    print("=" * 65)
    print(title.center(65))
    print("=" * 65)


# ===========================================================
# FIND PATIENT
# ===========================================================

def find_patient(pid):

    for patient in patients:

        if patient.pid.lower() == pid.lower():
            return patient

    return None


# ===========================================================
# FIND APPOINTMENT
# ===========================================================

def find_appointment(appointment_id):

    for appointment in appointments:

        if appointment.appointment_id.lower() == appointment_id.lower():
            return appointment

    return None


# ===========================================================
# GENERATE APPOINTMENT ID
# ===========================================================

def generate_appointment_id():

    number = len(appointments) + 1

    appointment_id = "A" + str(number).zfill(3)

    while find_appointment(appointment_id):

        number += 1
        appointment_id = "A" + str(number).zfill(3)

    return appointment_id


# ===========================================================
# REGISTER PATIENT
# ===========================================================

def register_patient():

    header("PATIENT REGISTRATION")

    pid = input("Patient ID       : ").strip()

    if pid == "":
        print("\nPatient ID cannot be empty.")
        return

    if find_patient(pid):

        print("\nPatient ID already exists.")
        print("Please enter a different Patient ID.")

        return

    name = input("Full Name        : ").strip()

    if name == "":
        print("\nName cannot be empty.")
        return

    age = input("Age              : ").strip()
    gender = input("Gender           : ").strip()
    phone = input("Phone Number     : ").strip()
    email = input("Email            : ").strip()
    address = input("Address          : ").strip()
    blood_group = input("Blood Group      : ").strip()
    allergies = input("Allergies        : ").strip()
    medical_history = input("Medical History  : ").strip()

    patient = Patient(
        pid,
        name,
        age,
        gender,
        phone,
        email,
        address,
        blood_group,
        allergies,
        medical_history
    )

    patients.append(patient)

    print("\n" + "=" * 65)
    print("Patient Registered Successfully!".center(65))
    print("=" * 65)


# ===========================================================
# DISPLAY PATIENT
# ===========================================================

def display_patient(patient):

    line()

    print("Patient ID       :", patient.pid)
    print("Name             :", patient.name)
    print("Age              :", patient.age)
    print("Gender           :", patient.gender)
    print("Phone            :", patient.phone)
    print("Email            :", patient.email)
    print("Address          :", patient.address)
    print("Blood Group      :", patient.blood_group)
    print("Allergies        :", patient.allergies)
    print("Medical History  :", patient.medical_history)

    line()


# ===========================================================
# VIEW ALL PATIENTS
# ===========================================================

def view_patients():

    header("ALL PATIENT RECORDS")

    if not patients:

        print("No patient records available.")

        return

    print("Total Patients:", len(patients))

    for patient in patients:

        display_patient(patient)


# ===========================================================
# SEARCH PATIENT
# ===========================================================

def search_patient():

    header("SEARCH PATIENT")

    pid = input("Enter Patient ID: ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found.")

        return

    print("\nPatient Information")
    display_patient(patient)


# ===========================================================
# UPDATE PATIENT
# ===========================================================

def update_patient():

    header("UPDATE PATIENT PROFILE")

    pid = input("Enter Patient ID: ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found.")

        return

    print("\nCurrent Patient Information:")
    display_patient(patient)

    print("\nEnter New Information")
    print("(Press Enter to keep the existing value.)\n")

    value = input("Name [%s]: " % patient.name).strip()

    if value:
        patient.name = value

    value = input("Age [%s]: " % patient.age).strip()

    if value:
        patient.age = value

    value = input("Gender [%s]: " % patient.gender).strip()

    if value:
        patient.gender = value

    value = input("Phone [%s]: " % patient.phone).strip()

    if value:
        patient.phone = value

    value = input("Email [%s]: " % patient.email).strip()

    if value:
        patient.email = value

    value = input("Address [%s]: " % patient.address).strip()

    if value:
        patient.address = value

    value = input("Blood Group [%s]: " % patient.blood_group).strip()

    if value:
        patient.blood_group = value

    value = input("Allergies [%s]: " % patient.allergies).strip()

    if value:
        patient.allergies = value

    value = input(
        "Medical History [%s]: " % patient.medical_history
    ).strip()

    if value:
        patient.medical_history = value

    print("\nPatient Profile Updated Successfully!")


# ===========================================================
# DELETE PATIENT
# ===========================================================

def delete_patient():

    header("DELETE PATIENT")

    pid = input("Enter Patient ID: ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found.")

        return

    print("\nPatient to be deleted:")
    display_patient(patient)

    confirmation = input(
        "Are you sure you want to delete this patient? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print("\nDeletion Cancelled.")

        return

    patients.remove(patient)

    # Delete all appointments belonging to this patient
    for appointment in appointments[:]:

        if appointment.pid.lower() == pid.lower():

            appointments.remove(appointment)

    print("\nPatient Deleted Successfully.")


# ===========================================================
# CHECK APPOINTMENT SLOT
# ===========================================================

def is_slot_available(doctor, date, time):

    for appointment in appointments:

        if appointment.status != "Cancelled":

            if (
                appointment.doctor.lower() == doctor.lower()
                and appointment.date.lower() == date.lower()
                and appointment.time.lower() == time.lower()
            ):

                return False

    return True


# ===========================================================
# BOOK APPOINTMENT
# ===========================================================

def book_appointment():

    header("APPOINTMENT SCHEDULING")

    pid = input("Patient ID       : ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found.")
        print("Please register the patient first.")

        return

    print("\nPatient:", patient.name)

    doctor = input("Doctor Name      : ").strip()

    if doctor == "":
        print("\nDoctor name cannot be empty.")
        return

    department = input("Department       : ").strip()
    date = input("Appointment Date : ").strip()
    time = input("Appointment Time : ").strip()
    reason = input("Reason for Visit : ").strip()

    # Check doctor/date/time availability
    if not is_slot_available(doctor, date, time):

        print("\n" + "=" * 65)
        print("SLOT ALREADY BOOKED".center(65))
        print("=" * 65)

        print("Doctor :", doctor)
        print("Date   :", date)
        print("Time   :", time)

        print("\nPlease select another time.")

        return

    appointment_id = generate_appointment_id()

    appointment = Appointment(
        appointment_id,
        pid,
        doctor,
        department,
        date,
        time,
        reason
    )

    appointments.append(appointment)

    print("\n" + "=" * 65)
    print("APPOINTMENT BOOKED SUCCESSFULLY".center(65))
    print("=" * 65)

    print("Appointment ID :", appointment_id)
    print("Patient        :", patient.name)
    print("Doctor         :", doctor)
    print("Department     :", department)
    print("Date           :", date)
    print("Time           :", time)
    print("Reason         :", reason)


# ===========================================================
# VIEW ALL APPOINTMENTS
# ===========================================================

def view_appointments():

    header("ALL APPOINTMENTS")

    if not appointments:

        print("No appointments available.")

        return

    for appointment in appointments:

        patient = find_patient(appointment.pid)

        line()

        print("Appointment ID :", appointment.appointment_id)

        if patient:
            print("Patient        :", patient.name)
        else:
            print("Patient ID     :", appointment.pid)

        print("Doctor         :", appointment.doctor)
        print("Department     :", appointment.department)
        print("Date           :", appointment.date)
        print("Time           :", appointment.time)
        print("Reason         :", appointment.reason)
        print("Status         :", appointment.status)

        line()


# ===========================================================
# SEARCH APPOINTMENT
# ===========================================================

def search_appointment():

    header("SEARCH APPOINTMENT")

    appointment_id = input("Appointment ID: ").strip()

    appointment = find_appointment(appointment_id)

    if appointment is None:

        print("\nAppointment Not Found.")

        return

    patient = find_patient(appointment.pid)

    print()

    line()

    print("Appointment ID :", appointment.appointment_id)

    if patient:
        print("Patient        :", patient.name)

    print("Patient ID     :", appointment.pid)
    print("Doctor         :", appointment.doctor)
    print("Department     :", appointment.department)
    print("Date           :", appointment.date)
    print("Time           :", appointment.time)
    print("Reason         :", appointment.reason)
    print("Status         :", appointment.status)

    line()


# ===========================================================
# CANCEL APPOINTMENT
# ===========================================================

def cancel_appointment():

    header("CANCEL APPOINTMENT")

    appointment_id = input(
        "Enter Appointment ID: "
    ).strip()

    appointment = find_appointment(appointment_id)

    if appointment is None:

        print("\nAppointment Not Found.")

        return

    if appointment.status == "Cancelled":

        print("\nThis appointment is already cancelled.")

        return

    patient = find_patient(appointment.pid)

    print("\nAppointment Details")

    line()

    if patient:
        print("Patient        :", patient.name)

    print("Appointment ID :", appointment.appointment_id)
    print("Doctor         :", appointment.doctor)
    print("Date           :", appointment.date)
    print("Time           :", appointment.time)

    line()

    confirmation = input(
        "Cancel this appointment? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        appointment.status = "Cancelled"

        print("\nAppointment Cancelled Successfully.")

    else:

        print("\nCancellation Aborted.")


# ===========================================================
# PATIENT APPOINTMENT HISTORY
# ===========================================================

def appointment_history():

    header("PATIENT APPOINTMENT HISTORY")

    pid = input("Enter Patient ID: ").strip()

    patient = find_patient(pid)

    if patient is None:

        print("\nPatient Not Found.")

        return

    print("\nPatient:", patient.name)

    found = False

    for appointment in appointments:

        if appointment.pid.lower() == pid.lower():

            found = True

            print()

            line()

            print("Appointment ID :", appointment.appointment_id)
            print("Doctor         :", appointment.doctor)
            print("Department     :", appointment.department)
            print("Date           :", appointment.date)
            print("Time           :", appointment.time)
            print("Reason         :", appointment.reason)
            print("Status         :", appointment.status)

            line()

    if not found:

        print("\nNo appointment history available.")


# ===========================================================
# AVAILABLE SLOT CHECK
# ===========================================================

def check_available_slot():

    header("CHECK APPOINTMENT SLOT")

    doctor = input("Doctor Name: ").strip()
    date = input("Date       : ").strip()
    time = input("Time       : ").strip()

    if is_slot_available(doctor, date, time):

        print("\nThe requested slot is AVAILABLE.")

    else:

        print("\nThe requested slot is NOT AVAILABLE.")


# ===========================================================
# DASHBOARD
# ===========================================================

def dashboard():

    header("MEDITRACK DASHBOARD")

    total_patients = len(patients)

    total_appointments = len(appointments)

    active_appointments = 0

    cancelled_appointments = 0

    for appointment in appointments:

        if appointment.status == "Booked":

            active_appointments += 1

        else:

            cancelled_appointments += 1

    print("Total Patients          :", total_patients)
    print("Total Appointments      :", total_appointments)
    print("Active Appointments    :", active_appointments)
    print("Cancelled Appointments :", cancelled_appointments)

    print("\nSystem Status: Operational")


# ===========================================================
# SAMPLE DATA
# ===========================================================

def load_sample_data():

    patient1 = Patient(
        "P001",
        "Rahul Kumar",
        "22",
        "Male",
        "9876543210",
        "rahul@gmail.com",
        "Warangal",
        "O+",
        "None",
        "No major medical history"
    )

    patient2 = Patient(
        "P002",
        "Anjali Sharma",
        "24",
        "Female",
        "9123456780",
        "anjali@gmail.com",
        "Hyderabad",
        "A+",
        "Dust allergy",
        "Asthma"
    )

    patients.append(patient1)
    patients.append(patient2)


# ===========================================================
# MAIN MENU
# ===========================================================

def main():

    while True:

        print("\n")
        print("=" * 65)
        print("             MEDITRACK PATIENT CARE SYSTEM")
        print("=" * 65)

        print("1.  Register Patient")
        print("2.  View All Patients")
        print("3.  Search Patient")
        print("4.  Update Patient Profile")
        print("5.  Delete Patient")
        print("6.  Book Appointment")
        print("7.  View All Appointments")
        print("8.  Search Appointment")
        print("9.  Cancel Appointment")
        print("10. Patient Appointment History")
        print("11. Check Appointment Slot")
        print("12. Dashboard")
        print("13. Load Sample Data")
        print("14. Exit")

        print("=" * 65)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            register_patient()

        elif choice == "2":

            view_patients()

        elif choice == "3":

            search_patient()

        elif choice == "4":

            update_patient()

        elif choice == "5":

            delete_patient()

        elif choice == "6":

            book_appointment()

        elif choice == "7":

            view_appointments()

        elif choice == "8":

            search_appointment()

        elif choice == "9":

            cancel_appointment()

        elif choice == "10":

            appointment_history()

        elif choice == "11":

            check_available_slot()

        elif choice == "12":

            dashboard()

        elif choice == "13":

            load_sample_data()

            print("\nSample data loaded successfully.")

        elif choice == "14":

            print("\nThank you for using MediTrack.")
            print("Program closed successfully.")

            break

        else:

            print("\nInvalid choice.")
            print("Please select an option from 1 to 14.")


# ===========================================================
# PROGRAM START
# ===========================================================

if __name__ == "__main__":

    main()

