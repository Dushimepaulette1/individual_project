#!/usr/bin/python3
import json

class Student:
    def __init__(self, email, names, courses_registered=None, GPA=0.0):
        self.email = email.strip().lower()
        self.names = names.strip()
        self.courses_registered = courses_registered if courses_registered is not None else []
        self.GPA = GPA

    def calculate_GPA(self):
        """
        Calculates the GPA based on the registered courses.
        If no courses are registered, sets GPA to 0.0.
        """
        if not self.courses_registered:
            self.GPA = 0.0
        else:
            # Calculate total credits and total points
            total_credits = sum(course['course_credits'] for course in self.courses_registered if course['grade'] is not None)
            total_points = sum(course['course_credits'] * course['grade'] for course in self.courses_registered if course['grade'] is not None)
            # Check to avoid division by zero
            self.GPA = total_points / total_credits if total_credits > 0 else 0.0

    def register_for_course(self, course):
        self.courses_registered.append(course)

    def to_dict(self):
        return {
            'email': self.email,
            'names': self.names,
            'courses_registered': self.courses_registered,
            'GPA': self.GPA
        }

class Course:
    def __init__(self, name, trimester, course_credits):
        self.name = name.strip()  # Course name
        self.trimester = trimester.strip()  # Trimester in which the course is offered
        self.course_credits = course_credits  # Credit hours for the course

    def to_dict(self):
        return {
            'name': self.name,
            'trimester': self.trimester,
            'course_credits': self.course_credits
        }

class GradeBook:
    def __init__(self):
        self.student_list = []  # List to store students
        self.course_list = []  # List to store courses
        self.load_data()  # Load data from files

    def add_student(self, email, names):
        # Check if a student with the same email already exists
        if not any(student.email == email for student in self.student_list):
            self.student_list.append(Student(email, names))  # Add a new student
            print("\nStudent added successfully.")
        else:
            print("\nStudent with this email already exists.")

    def add_course(self, name, trimester, course_credits):
        # Check if a course with the same name already exists
        if not any(course.name == name for course in self.course_list):
            self.course_list.append(Course(name, trimester, course_credits))  # Add a new course
            print("\nCourse added successfully.")
        else:
            print("\nCourse with this name already exists.")

    def register_student_for_course(self, email, course_name):
        print("\nRegistering student for course...")
        # Find the student and course by their identifiers
        student = next((s for s in self.student_list if s.email == email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        # Register the student for the course if both exist
        if student and course:
            student.register_for_course({'name': course.name, 'course_credits': course.course_credits, 'grade': None})
            print("\nCourse registered successfully.")
        else:
            print("\nError: Either the student or the course does not exist.")

    def register_grade(self, email, course_name, percentage_grade):
        print("\nRegistering grade for student...")
        student = next((s for s in self.student_list if s.email == email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            course_entry = next((c for c in student.courses_registered if c['name'] == course_name), None)
            if course_entry:
                course_entry['grade'] = self.convert_grade_to_gpa(percentage_grade)
                student.calculate_GPA()
                print("\nGrade registered successfully.")
            else:
                print("\nError: Course not found in student's registered courses.")
        else:
            print("\nError: Either the student or the course does not exist.")

    def convert_grade_to_gpa(self, percentage_grade):
        # Convert percentage grade to GPA based on predefined ranges
        if 90 <= percentage_grade <= 100:
            return 4.0
        elif 80 <= percentage_grade < 90:
            return 3.0
        elif 70 <= percentage_grade < 80:
            return 2.0
        elif 60 <= percentage_grade < 70:
            return 1.0
        else:
            return 0.0

    def calculate_GPA(self):
        print("\nCalculating GPA for all students...")
        # Calculate GPA for each student in the list
        for student in self.student_list:
            student.calculate_GPA()

    def calculate_ranking(self):
        self.calculate_GPA()  # Ensure all GPAs are up-to-date
        # Sort students by GPA in descending order
        ranked_students = sorted(self.student_list, key=lambda s: s.GPA, reverse=True)
        if ranked_students:
            print("\nStudent Ranking by GPA:")
            # Print each student's rank and GPA
            for rank, student in enumerate(ranked_students, start=1):
                print("{}. {}: {}".format(rank, student.email, student.GPA))
        else:
            print("\nNo students available to rank.")

    def search_by_grade(self, min_grade, max_grade):
        self.calculate_GPA()  # Ensure all GPAs are up-to-date
        # Filter students based on GPA range
        filtered_students = [s for s in self.student_list if min_grade <= s.GPA <= max_grade]
        if filtered_students:
            print("\nStudents in the GPA range:")
            # Print each student's email and GPA
            for student in filtered_students:
                print("{}: {}".format(student.email, student.GPA))
        else:
            print("\nNo students found in the specified GPA range.")

    def generate_transcript(self):
        self.calculate_GPA()  # Ensure all GPAs are up-to-date
        if self.student_list:
            # Sort students by GPA in descending order for the transcript
            ranked_students = sorted(self.student_list, key=lambda s: s.GPA, reverse=True)
            print("\nTranscript:")
            # Print each student's rank, names, and GPA
            for rank, student in enumerate(ranked_students, start=1):
                print("{}. {}".format(rank, student.names))
                print("GPA: {}\n".format(student.GPA))
        else:
            print("\nNo students available to generate transcripts.")

    def save_data(self):
        print("\nSaving data to files...")
        # Save student and course data to JSON files
        with open('students.json', 'w') as f:
            json.dump([student.to_dict() for student in self.student_list], f, indent=4)
        with open('courses.json', 'w') as f:
            json.dump([course.to_dict() for course in self.course_list], f, indent=4)

    def load_data(self):
        try:
            # Load student and course data from JSON files
            with open('students.json', 'r') as f:
                student_data = json.load(f)
                self.student_list = [Student(**data) for data in student_data]
            with open('courses.json', 'r') as f:
                course_data = json.load(f)
                self.course_list = [Course(**data) for data in course_data]
        except FileNotFoundError:
            # If files do not exist, start with empty lists
            pass

def get_valid_input(prompt, input_type=str):
    while True:
        user_input = input(prompt).strip()
        if input_type == str and not user_input.replace(' ', '').isdigit():
            return user_input
        elif input_type == int and user_input.isdigit():
            return int(user_input)
        elif input_type == float and user_input.replace('.', '', 1).isdigit():
            return float(user_input)
        else:
            print("Invalid input. Please enter a valid {}.".format(input_type.__name__))

def main():
    grade_book = GradeBook()

    while True:
        print("\n===================================")
        print("        Grade Book Menu")
        print("===================================")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Register Grade for Student")
        print("5. Calculate Ranking")
        print("6. Search by Grade")
        print("7. Generate Transcript")
        print("8. View Available Courses")
        print("9. Exit")
        print("===================================")

        choice = get_valid_input("Enter your choice: ", int)

        if choice == 1:
            print("\nAdding a new student...")
            email = get_valid_input("Enter student email: ")
            names = get_valid_input("Enter student names: ")
            grade_book.add_student(email, names)
        elif choice == 2:
            print("\nAdding a new course...")
            name = get_valid_input("Enter course name: ")
            trimester = get_valid_input("Enter course trimester: ")
            course_credits = get_valid_input("Enter course credits: ", int)
            grade_book.add_course(name, trimester, course_credits)
        elif choice == 3:
            print("\nRegistering a student for a course...")
            email = get_valid_input("Enter student email: ")
            course_name = get_valid_input("Enter course name: ")
            grade_book.register_student_for_course(email, course_name)
        elif choice == 4:
            print("\nRegistering a grade for a student...")
            email = get_valid_input("Enter student email: ")
            course_name = get_valid_input("Enter course name: ")
            percentage_grade = get_valid_input("Enter grade out of 100: ", float)
            grade_book.register_grade(email, course_name, percentage_grade)
        elif choice == 5:
            print("\nCalculating ranking...")
            grade_book.calculate_ranking()
        elif choice == 6:
            print("\nSearching by grade...")
            min_grade = get_valid_input("Enter minimum GPA: ", float)
            max_grade = get_valid_input("Enter maximum GPA: ", float)
            grade_book.search_by_grade(min_grade, max_grade)
        elif choice == 7:
            print("\nGenerating transcript...")
            grade_book.generate_transcript()
        elif choice == 8:
            print("\nAvailable Courses:")
            for course in grade_book.course_list:
                print("Course Name: {}".format(course.name))
        elif choice == 9:
            print("\nSaving data and exiting...")
            grade_book.save_data()
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()

