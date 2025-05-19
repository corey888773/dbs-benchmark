import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import math
import argparse
import os

fake = Faker()

def get_filepath(output_dir, filename):
    return os.path.join(output_dir, filename)

def generate_students_batch(start_id, batch_size, num_students):
    students = []
    end_id = min(start_id + batch_size, num_students + 1)
    for i in range(start_id, end_id):
        students.append([i, fake.first_name(), fake.last_name(), fake.date_of_birth(minimum_age=18, maximum_age=30), fake.date_time_this_decade()])
    return students

def generate_teachers_batch(start_id, batch_size, num_teachers):
    teachers = []
    end_id = min(start_id + batch_size, num_teachers + 1)
    for i in range(start_id, end_id):
        job = fake.job().replace(',', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        teachers.append([i, fake.first_name(), fake.last_name(), job, fake.date_this_decade(), fake.date_time_this_decade()])
    return teachers

def generate_classes_batch(start_id, batch_size, teachers, num_classes):
    classes = []
    end_id = min(start_id + batch_size, num_classes + 1)
    for i in range(start_id, end_id):
        classes.append([i, fake.word().capitalize(), random.choice(teachers)[0], fake.date_time_this_decade()])
    return classes

def generate_subjects_batch(start_id, batch_size, num_subjects):
    subjects = []
    end_id = min(start_id + batch_size, num_subjects + 1)
    for i in range(start_id, end_id):
        # replace newline with space
        subject_description = fake.text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(',', ' ').strip()
        subjects.append([i, fake.word().capitalize(), subject_description, fake.date_time_this_decade()])
    return subjects

def generate_grades_batch(start_id, batch_size, students, subjects, num_grades):
    grades = []
    end_id = min(start_id + batch_size, num_grades + 1)
    for i in range(start_id, end_id):
        grades.append([i, random.choice(students)[0], random.choice(subjects)[0], random.randint(1, 6), fake.date_time_this_decade()])
    return grades

def generate_enrollments_batch(batch_size, total_generated, students, classes, num_enrollments):
    enrollments = []
    remaining = min(batch_size, num_enrollments - total_generated)
    for _ in range(remaining):
        enrollments.append([random.choice(students)[0], random.choice(classes)[0], fake.date_time_this_decade()])
    return enrollments

def generate_schedules_batch(start_id, batch_size, classes, subjects, num_schedules):
    schedules = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    end_id = min(start_id + batch_size, num_schedules + 1)
    for i in range(start_id, end_id):
        time_start = fake.time_object()
        time_end = (datetime.combine(datetime.today(), time_start) + timedelta(hours=1)).time()
        schedules.append([i, random.choice(classes)[0], random.choice(subjects)[0], random.choice(days_of_week), time_start, time_end])
    return schedules

# Then modify save_to_csv_batch to accept output_dir
def save_to_csv_batch(filename, data, headers, output_dir='.', mode='a'):
    filepath = get_filepath(output_dir, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow(headers)
        writer.writerows(data)

# Update the process_entity_in_batches function signature with better parameter documentation
def process_entity_in_batches(total_count, batch_generator, filename, headers, depends_on=None, **kwargs):
    print(f"Processing {filename}...")
    num_batches = math.ceil(total_count / kwargs.get('batch_size', 10000))
    output_dir = kwargs.get('output_dir', '.')
    batch_size = kwargs.get('batch_size', 10000)
    
    # Create directory if it doesn't exist
    full_path = get_filepath(output_dir, filename)
    os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else '.', exist_ok=True)
    
    # First batch with headers
    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
    
    # Extract specific kwargs for the batch generator to avoid passing unwanted parameters
    batch_kwargs = {}
    if 'num_students' in kwargs:
        batch_kwargs['num_students'] = kwargs['num_students']
    if 'num_teachers' in kwargs:
        batch_kwargs['num_teachers'] = kwargs['num_teachers']
    if 'num_classes' in kwargs:
        batch_kwargs['num_classes'] = kwargs['num_classes']
    if 'num_subjects' in kwargs:
        batch_kwargs['num_subjects'] = kwargs['num_subjects']
    if 'num_grades' in kwargs:
        batch_kwargs['num_grades'] = kwargs['num_grades']
    if 'num_schedules' in kwargs:
        batch_kwargs['num_schedules'] = kwargs['num_schedules']
    if 'num_enrollments' in kwargs:
        batch_kwargs['num_enrollments'] = kwargs['num_enrollments']
    
    for i in range(num_batches):
        start_id = i * batch_size + 1
        if depends_on:
            batch = batch_generator(start_id, batch_size, *depends_on, **batch_kwargs)
        else:
            batch = batch_generator(start_id, batch_size, **batch_kwargs)
            
        with open(full_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(batch)
        print(f"  Batch {i+1}/{num_batches} processed for {filename}")

def generate_school_data(
    output_dir='.', 
    students_file='students.csv',
    teachers_file='teachers.csv',
    classes_file='classes.csv',
    subjects_file='subjects.csv',
    grades_file='grades.csv',
    enrollments_file='enrollments.csv',
    schedules_file='schedules.csv',
    scale=1000,
    batch_size=10000
):
    """
    Generate school data with the specified parameters.
    This function can be called directly from a Jupyter notebook.
    
    Parameters:
    -----------
    output_dir : str
        Directory to save CSV files
    students_file, teachers_file, etc. : str
        Filenames for each entity type
    scale : int
        Scale factor for data generation
    batch_size : int
        Batch size for data generation
    """
    # Entity counts based on proportions
    num_students = 10 * scale
    num_teachers = 5 * scale
    num_classes = 5 * scale
    num_subjects = 10 * scale
    num_grades = 30 * scale
    num_enrollments = 20 * scale
    num_schedules = 20 * scale
    
    # Generate reference data
    teachers = []
    for start_id in range(1, num_teachers + 1, batch_size):
        teachers.extend(generate_teachers_batch(
            start_id=start_id, 
            batch_size=batch_size, 
            num_teachers=num_teachers
        ))

    students = []
    for start_id in range(1, num_students + 1, batch_size):
        students.extend(generate_students_batch(
            start_id=start_id, 
            batch_size=batch_size, 
            num_students=num_students
        ))

    classes = []
    for start_id in range(1, num_classes + 1, batch_size):
        classes.extend(generate_classes_batch(
            start_id=start_id, 
            batch_size=batch_size, 
            teachers=teachers, 
            num_classes=num_classes
        ))

    subjects = []
    for start_id in range(1, num_subjects + 1, batch_size):
        subjects.extend(generate_subjects_batch(
            start_id=start_id, 
            batch_size=batch_size, 
            num_subjects=num_subjects
        ))

    # Process entities - pass just the filename, not the full path
    process_entity_in_batches(
        total_count=num_students, 
        batch_generator=generate_students_batch, 
        filename=students_file,  # Changed from get_filepath(students_file)
        headers=['id', 'first_name', 'last_name', 'birth_date', 'created_at'],
        num_students=num_students, 
        output_dir=output_dir,
        batch_size=batch_size
    )
                      
    process_entity_in_batches(
        total_count=num_teachers, 
        batch_generator=generate_teachers_batch, 
        filename=teachers_file,  # Changed from get_filepath(teachers_file)
        headers=['id', 'first_name', 'last_name', 'subject', 'hire_date', 'created_at'], 
        num_teachers=num_teachers, 
        output_dir=output_dir,
        batch_size=batch_size
    )
                      
    process_entity_in_batches(
        total_count=num_classes, 
        batch_generator=generate_classes_batch, 
        filename=classes_file, 
        headers=['id', 'name', 'teacher_id', 'created_at'], 
        depends_on=[teachers],
        num_classes=num_classes, 
        output_dir=output_dir,
        batch_size=batch_size
    )
                      
    process_entity_in_batches(
        total_count=num_subjects, 
        batch_generator=generate_subjects_batch, 
        filename=subjects_file,
        headers=['id', 'name', 'description', 'created_at'], 
        num_subjects=num_subjects, 
        output_dir=output_dir,
        batch_size=batch_size
    )
                      
    process_entity_in_batches(
        total_count=num_grades, 
        batch_generator=generate_grades_batch, 
        filename=grades_file,
        headers=['id', 'student_id', 'subject_id', 'grade', 'created_at'], 
        depends_on=[students, subjects],
        num_grades=num_grades, 
        output_dir=output_dir,
        batch_size=batch_size
    )
                      
    process_entity_in_batches(
        total_count=num_schedules, 
        batch_generator=generate_schedules_batch, 
        filename=schedules_file,
        headers=['id', 'class_id', 'subject_id', 'day_of_week', 'time_start', 'time_end'], 
        depends_on=[classes, subjects],
        num_schedules=num_schedules, 
        output_dir=output_dir,
        batch_size=batch_size
    )

    # Handle enrollments differently as they don't have sequential IDs
    print(f"Processing {enrollments_file}...")
    save_to_csv_batch(
        filename=enrollments_file,  # Changed from get_filepath(enrollments_file)
        data=[],
        headers=['student_id', 'class_id', 'enrolled_at'],
        output_dir=output_dir,
        mode='w'
    )

    total_enrollments = 0
    num_batches = math.ceil(num_enrollments / batch_size)
    for i in range(num_batches):
        batch = generate_enrollments_batch(
            batch_size=batch_size, 
            total_generated=total_enrollments, 
            students=students, 
            classes=classes, 
            num_enrollments=num_enrollments
        )
        save_to_csv_batch(
            filename=enrollments_file, 
            data=batch, 
            headers=[], 
            output_dir=output_dir,
            mode='a'
        )
        total_enrollments += len(batch)
        print(f"  Batch {i+1}/{num_batches} processed for {enrollments_file}")

    # Return generated data for use in notebook
    return {
        'students': students,
        'teachers': teachers,
        'classes': classes,
        'subjects': subjects
    }

# Main entry point for command line usage
if __name__ == "__main__":
    # Command line arguments setup
    parser = argparse.ArgumentParser(description='Generate CSV data files for database benchmarking')
    parser.add_argument('--output-dir', default='.', help='Directory to save CSV files')
    parser.add_argument('--students-file', default='students.csv', help='Filename for students data')
    parser.add_argument('--teachers-file', default='teachers.csv', help='Filename for teachers data') 
    parser.add_argument('--classes-file', default='classes.csv', help='Filename for classes data')
    parser.add_argument('--subjects-file', default='subjects.csv', help='Filename for subjects data')
    parser.add_argument('--grades-file', default='grades.csv', help='Filename for grades data')
    parser.add_argument('--enrollments-file', default='enrollments.csv', help='Filename for enrollments data')
    parser.add_argument('--schedules-file', default='schedules.csv', help='Filename for schedules data')
    parser.add_argument('--scale', type=int, default=1000, help='Scale factor for data generation')
    parser.add_argument('--batch-size', type=int, default=10000, help='Batch size for data generation')
    
    args = parser.parse_args()
    
    # Call the function with command line arguments
    generate_school_data(
        output_dir=args.output_dir,
        students_file=args.students_file,
        teachers_file=args.teachers_file,
        classes_file=args.classes_file,
        subjects_file=args.subjects_file,
        grades_file=args.grades_file,
        enrollments_file=args.enrollments_file,
        schedules_file=args.schedules_file,
        scale=args.scale,
        batch_size=args.batch_size
    )