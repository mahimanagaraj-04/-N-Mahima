class Student:
    def __init__(self, student_id, name, grade):
        self.id = student_id
        self.name = name
        self.grade = grade


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def list_students(self):
        for student in self.students:
            print("ID:", student.id)
            print("Name:", student.name)
            print("Grade:", student.grade)
            print("----------------")


manager = StudentManager()

student1 = Student(101, "Mahima", "A")
student2 = Student(102, "Rahul", "B")

manager.add_student(student1)
manager.add_student(student2)

manager.list_students()