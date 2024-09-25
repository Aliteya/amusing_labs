from database.db import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_student(db, name, age):
    new_student = Student(student_name=name, student_age=age)
    db.add(new_student)
    db.commit()
    logger.info("Student registered successfully.")

def login_student(db, name):
    student = db.query(Student).filter(Student.student_name == name).first()
    if student:
        logger.info(f"Student {student.student_name} logged in successfully.")
        return student
    else:
        logger.info("Student not found.")
        return None

def add_diploma(db, student_id, diploma_name, pages, count_sources):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        new_diploma = Diplom(diploma_name=diploma_name, pages=pages, count_sources=count_sources, student_id=student.student_id)
        db.add(new_diploma)
        db.commit()
        logger.info("Diploma added successfully.")
    else:
        logger.info("Student not found.")

def register_curator(db, name, age):
    new_curator = Curator(curator_name=name, curator_age=age)
    db.add(new_curator)
    db.commit()
    logger.info("Curator registered successfully.")

def view_diplomas(db):
    diplomas = db.query(Diplom).all()
    for diploma in diplomas:
        print(f"Diploma ID: {diploma.diploma_id}, Name: {diploma.diploma_name}, Pages: {diploma.pages}, Sources: {diploma.count_sources}")

def check_diploma(db, diploma_id):
    diploma = db.query(Diplom).filter(Diplom.diploma_id == diploma_id).first()
    if diploma:
        diploma.checked = True
        db.commit()
        logger.info("Diploma checked successfully.")
    else:
        logger.info("Diploma not found.")


def main():
    logger.info("Starting console application.")
    with Session(autocommit=False, autoflush=False, bind=engine) as db:
        while True:
            print("\nOptions:")
            print("1. Register Student")
            print("2. Login Student")
            print("3. Add Diploma")
            print("4. Register Curator")
            print("5. View Diplomas")
            print("6. Check Diploma")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter student name: ")
                age = int(input("Enter student age: "))
                register_student(db, name, age)
            elif choice == "2":
                name = input("Enter student name: ")
                login_student(db, name)
            elif choice == "3":
                student_id = int(input("Enter student ID: "))
                diploma_name = input("Enter diploma name: ")
                pages = int(input("Enter number of pages: "))
                count_sources = int(input("Enter number of sources: "))
                add_diploma(db, student_id, diploma_name, pages, count_sources)
            elif choice == "4":
                name = input("Enter curator name: ")
                age = int(input("Enter curator age: "))
                register_curator(db, name, age)
            elif choice == "5":
                view_diplomas(db)
            elif choice == "6":
                diploma_id = int(input("Enter diploma ID to check: "))
                check_diploma(db, diploma_id)
            elif choice == "7":
                logger.info("Exiting console application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()