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
    