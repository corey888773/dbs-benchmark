# Data Generator Usage

The `generator.py` script provides a flexible way to generate synthetic school data for database benchmarking. You can use it either from the command line or within a Jupyter notebook.

## Command Line Usage

To run the generator from the command line:

```bash
python generator.py [options]
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir` | `.` | Directory to save CSV files |
| `--students-file` | `students.csv` | Filename for students data |
| `--teachers-file` | `teachers.csv` | Filename for teachers data |
| `--classes-file` | `classes.csv` | Filename for classes data |
| `--subjects-file` | `subjects.csv` | Filename for subjects data |
| `--grades-file` | `grades.csv` | Filename for grades data |
| `--enrollments-file` | `enrollments.csv` | Filename for enrollments data |
| `--schedules-file` | `schedules.csv` | Filename for schedules data |
| `--scale` | `1000` | Scale factor for data generation |
| `--batch-size` | `10000` | Batch size for data generation |

### Examples

Generate data with default settings:
```bash
python generator.py
```

Generate data in a specific directory:
```bash
python generator.py --output-dir data/
```

Generate smaller dataset for testing:
```bash
python generator.py --output-dir data/small --scale 100
```

Generate data for a specific database with custom filenames:
```bash
python generator.py --output-dir data/mysql/ --students-file mysql_students.csv --scale 500
```

## Jupyter Notebook Usage

To use the generator in a Jupyter notebook:

```python
# Import the generator function
import sys
sys.path.append('/path/to/directory/containing/generator.py')
from generator import generate_school_data

# Generate data with default settings
result = generate_school_data()

# Generate data with custom settings
result = generate_school_data(
    output_dir='./data',
    scale=100,  # Smaller scale for testing
    batch_size=5000
)

# Access the generated reference data
students = result['students']
teachers = result['teachers'] 
classes = result['classes']
subjects = result['subjects']

# Print statistics
print(f"Generated {len(students)} students")
print(f"Generated {len(teachers)} teachers")
print(f"Generated {len(classes)} classes")
print(f"Generated {len(subjects)} subjects")

# Examine first student record
print(f"Sample student record: {students[0]}")
```

## Data Scaling

The `scale` parameter determines the size of the generated dataset using these proportions:

- Students: 10 × scale
- Teachers: 1 × scale
- Classes: 2 × scale
- Subjects: 1 × scale
- Grades: 30 × scale
- Enrollments: 20 × scale
- Schedules: 5 × scale

For example, with `scale=1000`, the generator will create 10,000 students, 1,000 teachers, etc.

## Batch Processing

The data is generated and written in batches to manage memory usage with large datasets. The default batch size is 10,000 records, but you can adjust this with the `--batch-size` option.
