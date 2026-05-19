from src.classes import Courses
from src.courseParser import CourseParser
from src.storage import CourseStorage

def main():
    my_courses = Courses()
    storage = CourseStorage("courses.json")
    
    my_courses.courses = storage.load()
    
    print("\n=== Hungarian University GPA Calculator ===")
    if my_courses.courses:
        print(f"📊 Loaded {len(my_courses.courses)} existing courses from database.")
        print(f"📈 Current Cumulative GPA: {my_courses.calculateGPA():.2f}")
    else:
        print("ℹ Starting fresh.")

    print("\nEnter your new courses below.")
    print("Format: [Name] [Credit] [Grade] [Term]")
    print("Example: Calculus 5 4 1")
    print("Commands: credits, score, total, term: (termID), add, change")
    print("Type 'done' or 'exit' to finish adding, calculate GPA, and save.\n")

    while True:
        user_input = input("Enter a command: ").strip()

        if not user_input:
            continue
        
        if user_input.lower() in ['done', 'exit']:
            break

        elif user_input.lower().startswith("term"):
            termID = int(user_input[-1])
            gpa = my_courses.calculateGPAByTerm(termID)

            print(f"\nTerm Cumulative Weighted GPA: {gpa:.2f}")

        elif user_input.lower() == "total":
            gpa = my_courses.calculateGPA()
            print(f"\nFinal Cumulative Weighted GPA: {gpa:.2f}")

        elif user_input.lower() == "score":
            print(f"\nTotal score: {my_courses.calculateTotal()[0]}")

        elif user_input.lower() == "credits":
            print(f"\nTotal credits: {my_courses.calculateTotal()[1]}")

        elif user_input.lower().startswith("add"):
            try:
                new_course = CourseParser.parse_input_line(user_input[3:])
                my_courses.addCourse(new_course)
                storage.save(my_courses.courses)
                print("-" * 30)

            except ValueError as error:
                print(f"{error}")
                print("-" * 30)

        else:
            print("Invalid Command!")

    print("\n" + "="*40)

if __name__ == "__main__":
    main()