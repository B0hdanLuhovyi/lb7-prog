import threading
import time

class Patient:
    id_counter = 1

    def __init__(self, name, age, history=None):
        self.id = Patient.id_counter
        Patient.id_counter += 1
        self.name = name
        self.age = age
        self.history = history or []

    def add_to_history(self, appointment):
        self.history.append(appointment)

    def __str__(self):
        return f"Пацієнт [ID: {self.id}] {self.name}, {self.age} років, Історія прийомів: {len(self.history)}"

class Doctor:
    id_counter = 1

    def __init__(self, name, specialization):
        self.id = Doctor.id_counter
        Doctor.id_counter += 1
        self.name = name
        self.specialization = specialization
        self.lock = threading.Lock()

    def __str__(self):
        return f"Лікар [ID: {self.id}] {self.name}, Спеціалізація: {self.specialization}"

class Diagnosis:
    def __init__(self, diagnosis_name, description=""):
        self.diagnosis_name = diagnosis_name
        self.description = description

    def __str__(self):
        return f"Діагноз: {self.diagnosis_name} ({self.description})"

class Prescription:
    def __init__(self, medicine_name, dosage):
        self.medicine_name = medicine_name
        self.dosage = dosage

    def __str__(self):
        return f"Призначення: {self.medicine_name}, Дозування: {self.dosage}"

class Appointment:
    id_counter = 1

    def __init__(self, patient, doctor):
        self.id = Appointment.id_counter
        Appointment.id_counter += 1
        self.patient = patient
        self.doctor = doctor
        self.diagnosis = None
        self.prescriptions = []

    def set_diagnosis(self, diagnosis):
        self.diagnosis = diagnosis

    def add_prescription(self, prescription):
        self.prescriptions.append(prescription)

    def __str__(self):
        result = f"Прийом [ID: {self.id}] Пацієнт: {self.patient.name}, Лікар: {self.doctor.name}\n"
        if self.diagnosis:
            result += f"  {self.diagnosis}\n"
        if self.prescriptions:
            result += "  Призначення:\n" + "\n".join(f"    - {p}" for p in self.prescriptions)
        return result

def make_appointment(patient, doctor, diagnosis, prescriptions):
    with doctor.lock:
        time.sleep(4)
        appointment = Appointment(patient, doctor)
        appointment.set_diagnosis(diagnosis)
        for prescription in prescriptions:
            appointment.add_prescription(prescription)
        patient.add_to_history(appointment)
        print(appointment)

if __name__ == '__main__':

    patient1 = Patient("Богдан Луговий", 19)
    patient2 = Patient("Вікторія Лугова", 44)
    doctor1 = Doctor("Анна Дьякова", "Терапевт")
    diagnosis1 = Diagnosis("ГРВІ", "Гостра респіраторна вірусна інфекція")
    prescription1 = Prescription("Парацетамол", "500 мг 2 рази на день")
    prescription2 = Prescription("Амізон", "1 таблетка 3 рази на день")
    diagnosis2 = Diagnosis("Гіпертонія", "Підвищений артеріальний тиск")
    prescription3 = Prescription("Еналаприл", "10 мг щодня")


    time_start = time.time()
    while True:

        t1 = threading.Thread(target=make_appointment, args=(patient1, doctor1, diagnosis1, [prescription1, prescription2]))

        t2 = threading.Thread(target=make_appointment, args=(patient2, doctor1, diagnosis2, [prescription3]))
    
        t1.start()

        t2.start()

        t1.join()
        t2.join()

        if time.time() - time_start >= 9:
            break
    print(patient1)
    print(patient2)

