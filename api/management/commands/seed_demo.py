from django.core.management.base import BaseCommand
from api.models import Student, Course, Lesson, Attempt, Question, Hint, QuestionAttempt
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **options):
        # Clear existing demo data
        Student.objects.filter(email="demo@student.com").delete()
        QuestionAttempt.objects.all().delete()
        Attempt.objects.all().delete()
        Question.objects.all().delete()
        Hint.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # Create student with ID 1 for frontend compatibility
        student = Student.objects.create(id=1, name="Demo Student", email="demo@student.com")

        # Create multiple courses with different progress levels
        courses_data = [
            {
                "name": "Python 101",
                "description": "Learn Python fundamentals",
                "difficulty": 2,
                "progress": 0.5,  # 50% complete
                "lessons": [
                    ("Intro to Variables", ["python", "variables"]),
                    ("Loops and Control Flow", ["python", "loops"]),
                    ("Functions and Modules", ["python", "functions"]),
                    ("Data Structures", ["python", "lists", "dictionaries"]),
                ]
            },
            {
                "name": "JavaScript Essentials",
                "description": "Master JavaScript programming",
                "difficulty": 3,
                "progress": 0.0,  # Not started
                "lessons": [
                    ("Variables and Data Types", ["javascript", "variables"]),
                    ("Functions and Scope", ["javascript", "functions"]),
                    ("Arrays and Objects", ["javascript", "arrays"]),
                    ("DOM Manipulation", ["javascript", "dom"]),
                ]
            },
            {
                "name": "Web Development",
                "description": "Build modern web applications",
                "difficulty": 4,
                "progress": 0.75,  # 75% complete
                "lessons": [
                    ("HTML Fundamentals", ["html", "markup"]),
                    ("CSS Styling", ["css", "styling"]),
                    ("JavaScript Events", ["javascript", "events"]),
                    ("Responsive Design", ["css", "responsive"]),
                    ("API Integration", ["javascript", "api"]),
                ]
            },
            {
                "name": "Data Science with Python",
                "description": "Analyze data with Python libraries",
                "difficulty": 5,
                "progress": 0.25,  # 25% complete
                "lessons": [
                    ("NumPy Basics", ["python", "numpy", "data"]),
                    ("Pandas DataFrames", ["python", "pandas", "data"]),
                    ("Data Visualization", ["python", "matplotlib", "charts"]),
                    ("Statistical Analysis", ["python", "statistics"]),
                ]
            },
            {
                "name": "Machine Learning Fundamentals",
                "description": "Introduction to ML algorithms",
                "difficulty": 5,
                "progress": 0.0,  # Not started
                "lessons": [
                    ("Linear Regression", ["ml", "regression"]),
                    ("Classification Algorithms", ["ml", "classification"]),
                    ("Neural Networks", ["ml", "neural-networks"]),
                    ("Model Evaluation", ["ml", "evaluation"]),
                ]
            }
        ]

        courses = []
        for course_data in courses_data:
            course = Course.objects.create(
                name=course_data["name"],
                description=course_data["description"],
                difficulty=course_data["difficulty"]
            )

            # Create lessons for this course
            lessons = []
            for i, (lesson_title, lesson_tags) in enumerate(course_data["lessons"]):
                lesson = Lesson.objects.create(
                    course=course,
                    title=lesson_title,
                    tags=lesson_tags,
                    order_index=i + 1
                )
                lessons.append(lesson)

            courses.append((course, course_data, lessons))

        # Create sample attempts for different progress levels
        for course, course_data, lessons in courses:
            progress = course_data["progress"]
            if progress > 0:
                # Create attempts for completed lessons
                completed_lessons = int(len(lessons) * progress)
                for i in range(completed_lessons):
                    Attempt.objects.create(
                        student=student,
                        lesson=lessons[i],
                        correctness=0.8 + (i * 0.05),  # Varying correctness
                        hints_used=min(i, 2),  # Some hints used
                        duration_sec=200 + (i * 30)
                    )

        # Get the first lesson of the first course for creating questions
        first_course, first_course_data, first_course_lessons = courses[0]
        lesson1 = first_course_lessons[0]
        lesson2 = first_course_lessons[1]

        # Create questions for lesson 1 (Python 101 - Intro to Variables)
        question1 = Question.objects.create(
            lesson=lesson1,
            question_type='mcq',
            title="Variable Declaration",
            content="Which of the following is the correct way to declare a variable in Python?",
            options=[
                "A) var x = 5",
                "B) x := 5",
                "C) x = 5",
                "D) let x = 5"
            ],
            correct_answer=["C"],
            difficulty=1,
            points=10,
            order_index=1,
            tags=["variables", "syntax"]
        )

        # Add hints for question 1
        Hint.objects.create(
            question=question1,
            content="Python uses simple assignment with the = operator.",
            order_index=1,
            penalty_points=2
        )
        Hint.objects.create(
            question=question1,
            content="Unlike JavaScript, Python doesn't use var, let, or const keywords.",
            order_index=2,
            penalty_points=3
        )

        question2 = Question.objects.create(
            lesson=lesson1,
            question_type='mcq',
            title="Data Types",
            content="What is the data type of the value 'Hello World' in Python?",
            options=[
                "A) int",
                "B) float",
                "C) str",
                "D) bool"
            ],
            correct_answer=["C"],
            difficulty=1,
            points=10,
            order_index=2,
            tags=["data-types", "strings"]
        )

        # Add hints for question 2
        Hint.objects.create(
            question=question2,
            content="Text enclosed in quotes is called a string.",
            order_index=1,
            penalty_points=1
        )

        # Create questions for lesson 2 (Python 101 - Loops and Control Flow)
        question3 = Question.objects.create(
            lesson=lesson2,
            question_type='mcq',
            title="For Loop Syntax",
            content="Which of the following is the correct syntax for a for loop in Python?",
            options=[
                "A) for i in range(5):",
                "B) for (int i = 0; i < 5; i++):",
                "C) foreach i in 0..5:",
                "D) for i = 0 to 5:"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["loops", "syntax"]
        )

        # Add hints for question 3
        Hint.objects.create(
            question=question3,
            content="Python uses 'in' to iterate over sequences.",
            order_index=1,
            penalty_points=2
        )
        Hint.objects.create(
            question=question3,
            content="The range() function generates a sequence of numbers.",
            order_index=2,
            penalty_points=3
        )

        # Create a coding question
        question4 = Question.objects.create(
            lesson=lesson2,
            question_type='coding',
            title="Simple Loop",
            content="Write a Python function that takes a number n and returns the sum of all numbers from 1 to n.",
            options=None,
            correct_answer=[{"test_cases": [
                {"input": 5, "expected": 15},
                {"input": 10, "expected": 55}
            ]}],
            difficulty=2,
            points=20,
            order_index=2,
            tags=["loops", "functions"]
        )

        # Add hints for coding question
        Hint.objects.create(
            question=question4,
            content="Use a for loop with range(1, n+1) to iterate from 1 to n.",
            order_index=1,
            penalty_points=3
        )
        Hint.objects.create(
            question=question4,
            content="Initialize a variable sum = 0 before the loop and add each number to it.",
            order_index=2,
            penalty_points=4
        )

        # Create some question attempts
        QuestionAttempt.objects.create(
            student=student,
            question=question1,
            answer=["C"],
            is_correct=True,
            hints_used=0,
            duration_sec=45,
            points_earned=10
        )

        QuestionAttempt.objects.create(
            student=student,
            question=question2,
            answer=["C"],
            is_correct=True,
            hints_used=1,
            duration_sec=30,
            points_earned=9  # 10 - 1 hint penalty
        )

        self.stdout.write(self.style.SUCCESS("Demo data created with questions and hints"))
