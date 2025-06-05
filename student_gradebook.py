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

student_gradebook_stats()  # Call the function to display stats initially #testing purposes