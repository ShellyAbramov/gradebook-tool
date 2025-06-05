student_grades = {} #empty dictionary to store student names and grades

def student_info(): 
    """Function to get student information from user input.
    And add a key-value pair to the dictionary student_grades containing the student's full name and grade."""

    student_full_name = input("Enter the student's full name: ")
    try:
        grade = float(input("Enter the student's grade: "))
        student_grades[student_full_name] = grade
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

def student_letter_grade():
    """Function to display the letter grade for each student based on their numeric grade."""
    if not student_grades:
        print("No students in the gradebook.")
    else:
        print("\nStudent Letter Grades:")
        for student, grade in student_grades.items():
            if grade >= 98:
                letter_grade = 'A+'
            elif grade >= 92:
                letter_grade = 'A'
            elif grade >= 90:
                letter_grade = 'A-'
            elif grade >= 88:
                letter_grade = 'B+'
            elif grade >= 82:
                letter_grade = 'B'
            elif grade >= 80:
                letter_grade = 'B-'
            elif grade >= 78:
                letter_grade = 'C+'
            elif grade >= 72:
                letter_grade = 'C'
            elif grade >= 70:
                letter_grade = 'C-'
            elif grade >= 68:
                letter_grade = 'D+'
            elif grade >= 62:
                letter_grade = 'D'
            elif grade >= 60:
                letter_grade = 'D-'
            else:
                letter_grade = 'F'
            print(f"{student}: {letter_grade}")

# student_letter_grade()  # Call the function to display letter grades initially #testing purposes

def main():
    """Main function to run the student gradebook program."""
    while True:
        print("\nStudent Gradebook Menu:")
        print("1. Add Student Info")
        print("2. Display Gradebook Stats")
        print("3. Display Letter Grades")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            student_info()
        elif choice == '2':
            student_gradebook_stats()
        elif choice == '3':
            student_letter_grade()
        elif choice == '4':
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  