student_grades = {} #empty dictionary to store student names and grades

def student_info(): 
    """Function to get student information from user input.
    And add a key-value pair to the dictionary student_grades containing the student's full name and grade."""

    student_full_name = input("Enter the student's full name: ")
    while True:
        try:
            grade = float(input("Enter the student's grade: "))
            if grade < 0 or grade > 100:
                print("Grade must be between 0 and 100. Please try again.")
                continue # Loop until a valid grade is entered
            student_grades[student_full_name] = grade
            break
        except ValueError:
            print("Invalid input. Please enter a valid numeric grade.")
#     print(f"Student {student_full_name} with grade {grade} added successfully.") #for testing purposes
# student_info() #call the function to get student information #for testing purposes
    
def student_gradebook_stats():
    """Function to display the stats of student gradebook including min, max, and average grade."""
    if not student_grades:
        print("No students in the gradebook.")
    else:
        print("\nStudent Gradebook Statistics:")
        grades = student_grades.values()
        length = len(grades)
        if length > 0:
            min_grade = min(grades)
            max_grade = max(grades)
            avg_grade = sum(grades) / length
            print(f"Minimum Grade: {min_grade}")
            print(f"Maximum Grade: {max_grade}")
            print(f"Average Grade: {avg_grade:.2f}")
        else:
            print("No grades available to calculate statistics.")

# student_gradebook_stats()  # Call the function to display stats initially #testing purposes

def get_letter_grade(grade):
    """Helper function to convert numeric grade to letter grade using mapping."""
    grade_map = {
        10: 'A+',
        9: 'A',
        8: 'B',
        7: 'C',
        6: 'D'
    }
    return grade_map.get(grade // 10, 'F')


def student_letter_grade():
    """Function to display the letter grade for each student based on their numeric grade."""
    if not student_grades:
        print("No students in the gradebook.")
    else:
        print("\nStudent Letter Grades:")
        for student, grade in student_grades.items():
            letter_grade = get_letter_grade(grade)
            print(f"{student}: {letter_grade}")

# student_letter_grade()  # Call the function to display letter grades initially #testing purposes

def save_gradebook_to_file(filename="student_gradebook.txt"):
    """Function to save the student gradebook to a file. (writing to a file)"""
    with open(filename, 'w') as file:
        for student, grade in student_grades.items():
            file.write(f"{student}: {grade}\n")
    print(f"Gradebook saved to {filename}") #for testing purposes

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


def main():
    """Main function to run the student gradebook program."""
    while True:
        print("\nStudent Gradebook Menu:")
        print("1. Add Student Info")
        print("2. Display Gradebook Stats")
        print("3. Display Letter Grades")
        print("4. Save Gradebook to File")
        print("5. Calculate Gradebook Stats from File")
        print("6. Exit")
        
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            student_info()
        elif choice == '2':
            student_gradebook_stats()
        elif choice == '3':
            student_letter_grade()
        elif choice == '4':
            save_gradebook_to_file()
        elif choice == '5':
            calculate_stats_from_file()
        elif choice == '6':
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  