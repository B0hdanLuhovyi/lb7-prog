import unittest
import threading
import time
from test import Patient, Doctor, Diagnosis, Prescription, Appointment, make_appointment

class TestMedicalAppointments(unittest.TestCase):

    def setUp(self):
        self.patient = Patient("Богдан Луговий", 19)
        self.doctor = Doctor("Анна Дьякова", "Терапевт")
        self.diagnosis = Diagnosis("ГРВІ", "Гостра респіраторна вірусна інфекція")
        self.prescription1 = Prescription("Парацетамол", "500 мг 2 рази на день")
        self.prescription2 = Prescription("Амізон", "1 таблетка 3 рази на день")
    
    def test_patient_creation(self):
        self.assertEqual(self.patient.name, "Богдан Луговий")
        self.assertEqual(self.patient.age, 19)
        self.assertEqual(len(self.patient.history), 0)

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.name, "Анна Дьякова")
        self.assertEqual(self.doctor.specialization, "Терапевт")

    def test_diagnosis_creation(self):
        self.assertEqual(self.diagnosis.diagnosis_name, "ГРВІ")
        self.assertEqual(self.diagnosis.description, "Гостра респіраторна вірусна інфекція")
    
    def test_prescription_creation(self):
        self.assertEqual(self.prescription1.medicine_name, "Парацетамол")
        self.assertEqual(self.prescription1.dosage, "500 мг 2 рази на день")
    
    def test_appointment_creation(self):
        appointment = Appointment(self.patient, self.doctor)
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertIsNone(appointment.diagnosis)
        self.assertEqual(len(appointment.prescriptions), 0)
    
    def test_appointment_process(self):
        t1 = threading.Thread(target=make_appointment, args=(self.patient, self.doctor, self.diagnosis, [self.prescription1, self.prescription2]))
        t1.start()
        t1.join()
        self.assertEqual(len(self.patient.history), 1)
        self.assertEqual(self.patient.history[0].diagnosis.diagnosis_name, "ГРВІ")
        self.assertEqual(len(self.patient.history[0].prescriptions), 2)

if __name__ == '__main__':
    unittest.main()
