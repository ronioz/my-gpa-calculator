from src.classes import Course

class CourseParser:
    @staticmethod
    def parse_input_line(user_input: str) -> Course:
        """
        Parses a single input string into a Course object.
        Expected format: [Name with spaces] [Credit] [Grade] [Term]
        Raises ValueError with custom messages if validation fails.
        """
        cleaned_input = user_input.strip()
        if not cleaned_input:
            raise ValueError("Input is empty.")

        parts = cleaned_input.split()
        
        if len(parts) < 4:
            raise ValueError("Missing information. Please enter: Name Credit Grade Term")

        course_name = " ".join(parts[:-3])
        
        try:
            credit = int(parts[-3])
            score = int(parts[-2])
            term = int(parts[-1])
            
        except ValueError:
            raise ValueError("Formatting error. Credit, Grade, and Term must be integers.")

        if score < 1 or score > 5:
            raise ValueError("Hungarian grades must be integers between 1 and 5.")
        if credit <= 0:
            raise ValueError("Credits must be greater than 0.")
        if term <= 0:
            raise ValueError("Term ID must be a positive integer.")

        return Course(course_name, credit, score, term)