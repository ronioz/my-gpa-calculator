class Course:
    def __init__(self, courseName: str, credit: int, score: int, termID: int) -> None:
        self.courseName = courseName
        self.credit = credit
        self.score = score 
        self.termID = termID 

    def changeCourseName(self, newName: str) -> None:
        if newName is None:
            print("Enter name")
            return

        self.courseName = newName 

    def changeCredit(self, newCredit: int) -> None:
        if newCredit <= 0:
            print("Enter valid credit")
            return
        
        self.credit = newCredit

    def changeScore(self, newScore: int) -> None:
        if newScore < 1 or newScore > 5:
            print("Enter valid score (1-5)")
            return
         
        self.score = newScore

    def changeTerm(self, newTerm: int) -> None:
        if not 1<= newTerm <= 6:
            print("Enter valid term")
            return
        
        self.termID = newTerm

    def __str__(self) -> str:
        return f"Name: {self.courseName}, credit: {self.credit}, score: {self.score}, term: {self.termID}"
    
    def to_dict(self) -> dict:
        return {
            "course_name": self.courseName,
            "credit": self.credit,
            "score": self.score,
            "term_id": self.termID
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["course_name"], data["credit"], data["score"], data["term_id"])
    
class Courses:
    def __init__(self) -> None:
        self.courses = {}

    def addCourse(self, course: Course) -> None:
        if course.courseName in self.courses:
            print(f"⚠ Course '{course.courseName}' already exists!")
            return
        self.courses[course.courseName] = course
        print(f"Added {course.courseName} successfully.")

    def removeCourse(self, courseName: str) -> None:
        if courseName not in self.courses:
            print(f"Enter valid course name")
            return
        
        self.courses.pop(courseName)
        print(f"Removed {courseName} successfully.")

    def calculateTotal(self) -> tuple:
        totalScore = 0
        totalCredit = 0
        for course in self.courses.values():
            totalScore += course.score * course.credit
            totalCredit += course.credit
        return totalScore, totalCredit
    
    def calculateGPA(self) -> float:
        totalScore, totalCredit = self.calculateTotal()
        
        if totalCredit == 0:
            return 0.0
        
        return totalScore / totalCredit
    
    def calculateGPAByTerm(self, n: int) -> float:
        termScore, termCredit = 0, 0

        for course in self.courses.values():
            if course.termID == n:
                termScore += course.credit * course.score
                termCredit += course.credit

        if termCredit == 0:
            return 0.0
        
        return termScore / termCredit