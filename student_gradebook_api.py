
def add_student_info(name, grade): #for API input
    """Function to add student information to the gradebook."""
    student_grades[name] = grade
    save_gradebook_to_file()  # Save to file after adding a student

def calculate_stats_from_file(file_name="student_gradebook.txt"):
    """Function that reads from file and calculates the stats of student gradebook including min, max, and average grade.(reading from a file)"""
    grades = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    try:
                        grade = float(parts[1].strip())
                        grades.append(grade)
                    except ValueError:
                        continue  # Skips lines with invalid grades
        if grades:
            min_grade = min(grades)
            max_grade = max(grades)
            avg_grade = sum(grades) / len(grades)
            print(f"Minimum Grade: {min_grade:.2f}")
            print(f"Maximum Grade: {max_grade:.2f}")
            print(f"Average Grade: {avg_grade:.2f}")
        else:
            print("No valid grades found in the file.")
    except FileNotFoundError:
        print(f'File {file_name} not found. Please ensure the file exists.')

    return {
    "min_grade": min_grade,
    "max_grade": max_grade,
    "avg_grade": avg_grade
    }