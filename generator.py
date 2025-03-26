import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

NUM_STUDENTS = 100
NUM_TEACHERS = 10
NUM_CLASSES = 20
NUM_SUBJECTS = 10
NUM_GRADES = 300
NUM_ENROLLMENTS = 200
NUM_SCHEDULES = 50

def generate_students():
    students = []
    for i in range(1, NUM_STUDENTS + 1):
        students.append([i, fake.first_name(), fake.last_name(), fake.date_of_birth(minimum_age=18, maximum_age=30), fake.date_time_this_decade()])
    return students

def generate_teachers():
    teachers = []
    for i in range(1, NUM_TEACHERS + 1):
        teachers.append([i, fake.first_name(), fake.last_name(), fake.job(), fake.date_this_decade(), fake.date_time_this_decade()])
    return teachers

def generate_classes(teachers):
    classes = []
    for i in range(1, NUM_CLASSES + 1):
        classes.append([i, fake.word().capitalize(), random.choice(teachers)[0], fake.date_time_this_decade()])
    return classes

def generate_subjects():
    subjects = []
    for i in range(1, NUM_SUBJECTS + 1):
        subjects.append([i, fake.word().capitalize(), fake.text(), fake.date_time_this_decade()])
    return subjects

def generate_grades(students, subjects):
    grades = []
    for i in range(1, NUM_GRADES + 1):
        grades.append([i, random.choice(students)[0], random.choice(subjects)[0], random.randint(1, 6), fake.date_time_this_decade()])
    return grades

def generate_enrollments(students, classes):
    enrollments = []
    for _ in range(NUM_ENROLLMENTS):
        enrollments.append([random.choice(students)[0], random.choice(classes)[0], fake.date_time_this_decade()])
    return enrollments

def generate_schedules(classes, subjects):
    schedules = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i in range(1, NUM_SCHEDULES + 1):
        time_start = fake.time_object()
        time_end = (datetime.combine(datetime.today(), time_start) + timedelta(hours=1)).time()
        schedules.append([i, random.choice(classes)[0], random.choice(subjects)[0], random.choice(days_of_week), time_start, time_end])
    return schedules

def save_to_csv(filename, data, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

students = generate_students()
teachers = generate_teachers()
classes = generate_classes(teachers)
subjects = generate_subjects()
grades = generate_grades(students, subjects)
enrollments = generate_enrollments(students, classes)
schedules = generate_schedules(classes, subjects)

save_to_csv('students.csv', students, ['id', 'first_name', 'last_name', 'birth_date', 'created_at'])
save_to_csv('teachers.csv', teachers, ['id', 'first_name', 'last_name', 'subject', 'hire_date', 'created_at'])
save_to_csv('classes.csv', classes, ['id', 'name', 'teacher_id', 'created_at'])
save_to_csv('subjects.csv', subjects, ['id', 'name', 'description', 'created_at'])
save_to_csv('grades.csv', grades, ['id', 'student_id', 'subject_id', 'grade', 'created_at'])
save_to_csv('enrollments.csv', enrollments, ['student_id', 'class_id', 'enrolled_at'])
save_to_csv('schedules.csv', schedules, ['id', 'class_id', 'subject_id', 'day_of_week', 'time_start', 'time_end'])

print("Pliki CSV zostały wygenerowane!")
