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
                    ("Object-Oriented Programming", ["python", "oop", "classes"]),
                    ("File Handling and Exceptions", ["python", "files", "exceptions"]),
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
                "name": "Machine Learning",
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

        # Create questions for all courses and lessons
        self.create_questions_for_all_courses(courses, student)

        self.stdout.write(self.style.SUCCESS("Demo data created with questions and hints"))

    def create_questions_for_all_courses(self, courses, student):
        """Create questions for all courses and lessons"""
        
        # Python 101 Questions
        python_course = courses[0][0]
        python_lessons = courses[0][2]
        
        # Intro to Variables
        self.create_python_variables_questions(python_lessons[0], student)
        
        # Loops and Control Flow
        self.create_python_loops_questions(python_lessons[1], student)
        
        # Functions and Modules
        self.create_python_functions_questions(python_lessons[2], student)
        
        # Data Structures
        self.create_python_data_structures_questions(python_lessons[3], student)
        
        # Object-Oriented Programming
        self.create_python_oop_questions(python_lessons[4], student)
        
        # File Handling and Exceptions
        self.create_python_files_questions(python_lessons[5], student)
        
        # JavaScript Essentials Questions
        js_course = courses[1][0]
        js_lessons = courses[1][2]
        
        # Variables and Data Types
        self.create_js_variables_questions(js_lessons[0], student)
        
        # Functions and Scope
        self.create_js_functions_questions(js_lessons[1], student)
        
        # Arrays and Objects
        self.create_js_arrays_questions(js_lessons[2], student)
        
        # DOM Manipulation
        self.create_js_dom_questions(js_lessons[3], student)
        
        # Web Development Questions
        web_course = courses[2][0]
        web_lessons = courses[2][2]
        
        # HTML Fundamentals
        self.create_html_questions(web_lessons[0], student)
        
        # CSS Styling
        self.create_css_questions(web_lessons[1], student)
        
        # JavaScript Events
        self.create_js_events_questions(web_lessons[2], student)
        
        # Responsive Design
        self.create_responsive_questions(web_lessons[3], student)
        
        # API Integration
        self.create_api_questions(web_lessons[4], student)
        
        # Data Science Questions
        ds_course = courses[3][0]
        ds_lessons = courses[3][2]
        
        # NumPy Basics
        self.create_numpy_questions(ds_lessons[0], student)
        
        # Pandas DataFrames
        self.create_pandas_questions(ds_lessons[1], student)
        
        # Data Visualization
        self.create_visualization_questions(ds_lessons[2], student)
        
        # Statistical Analysis
        self.create_statistics_questions(ds_lessons[3], student)
        
        # Machine Learning Questions
        ml_course = courses[4][0]
        ml_lessons = courses[4][2]
        
        # Linear Regression
        self.create_linear_regression_questions(ml_lessons[0], student)
        
        # Classification Algorithms
        self.create_classification_questions(ml_lessons[1], student)
        
        # Neural Networks
        self.create_neural_networks_questions(ml_lessons[2], student)
        
        # Model Evaluation
        self.create_model_evaluation_questions(ml_lessons[3], student)

    def create_python_variables_questions(self, lesson, student):
        """Create questions for Python Variables lesson"""
        # Question 1: Variable Declaration
        q1 = Question.objects.create(
            lesson=lesson,
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
        
        Hint.objects.create(question=q1, content="Python uses simple assignment with the = operator.", order_index=1, penalty_points=2)
        Hint.objects.create(question=q1, content="Unlike JavaScript, Python doesn't use var, let, or const keywords.", order_index=2, penalty_points=3)
        
        # Question 2: Data Types
        q2 = Question.objects.create(
            lesson=lesson,
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
        
        Hint.objects.create(question=q2, content="Text enclosed in quotes is called a string.", order_index=1, penalty_points=1)
        
        # Question 3: Variable Naming
        q3 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Variable Naming",
            content="Which of the following is a valid variable name in Python?",
            options=[
                "A) 2my_var",
                "B) my-var",
                "C) my_var",
                "D) my var"
            ],
            correct_answer=["C"],
            difficulty=1,
            points=10,
            order_index=3,
            tags=["variables", "naming"]
        )
        
        Hint.objects.create(question=q3, content="Variable names cannot start with numbers or contain spaces or hyphens.", order_index=1, penalty_points=2)

    def create_python_loops_questions(self, lesson, student):
        """Create questions for Python Loops lesson"""
        # Question 1: For Loop Syntax
        q1 = Question.objects.create(
            lesson=lesson,
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
        
        Hint.objects.create(question=q1, content="Python uses 'in' to iterate over sequences.", order_index=1, penalty_points=2)
        Hint.objects.create(question=q1, content="The range() function generates a sequence of numbers.", order_index=2, penalty_points=3)
        
        # Question 2: Coding Question
        q2 = Question.objects.create(
            lesson=lesson,
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
        
        Hint.objects.create(question=q2, content="Use a for loop with range(1, n+1) to iterate from 1 to n.", order_index=1, penalty_points=3)
        Hint.objects.create(question=q2, content="Initialize a variable sum = 0 before the loop and add each number to it.", order_index=2, penalty_points=4)

    def create_python_functions_questions(self, lesson, student):
        """Create questions for Python Functions lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Function Definition",
            content="What keyword is used to define a function in Python?",
            options=[
                "A) function",
                "B) def",
                "C) func",
                "D) define"
            ],
            correct_answer=["B"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["functions", "syntax"]
        )
        
        Hint.objects.create(question=q1, content="Python uses 'def' followed by the function name and parameters.", order_index=1, penalty_points=2)

    def create_python_data_structures_questions(self, lesson, student):
        """Create questions for Python Data Structures lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="List Creation",
            content="How do you create an empty list in Python?",
            options=[
                "A) list()",
                "B) []",
                "C) Both A and B",
                "D) None of the above"
            ],
            correct_answer=["C"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["lists", "data-structures"]
        )
        
        Hint.objects.create(question=q1, content="Both list() and [] create empty lists.", order_index=1, penalty_points=2)

    def create_python_oop_questions(self, lesson, student):
        """Create questions for Python Object-Oriented Programming lesson"""
        # Question 1: Class Definition
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Class Definition",
            content="What keyword is used to define a class in Python?",
            options=[
                "A) class",
                "B) def",
                "C) struct",
                "D) object"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["oop", "classes"]
        )
        
        Hint.objects.create(question=q1, content="Python uses 'class' followed by the class name.", order_index=1, penalty_points=2)
        
        # Question 2: Constructor Method
        q2 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Constructor Method",
            content="What is the name of the special method used to initialize a class instance?",
            options=[
                "A) __init__",
                "B) __new__",
                "C) __construct__",
                "D) __start__"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=2,
            tags=["oop", "constructor"]
        )
        
        Hint.objects.create(question=q2, content="__init__ is the constructor method in Python classes.", order_index=1, penalty_points=2)
        
        # Question 3: Instance Variables
        q3 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Instance Variables",
            content="How do you access an instance variable in Python?",
            options=[
                "A) self.variable_name",
                "B) this.variable_name",
                "C) instance.variable_name",
                "D) obj.variable_name"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=3,
            tags=["oop", "instance-variables"]
        )
        
        Hint.objects.create(question=q3, content="Use 'self' to refer to the current instance of the class.", order_index=1, penalty_points=2)

    def create_python_files_questions(self, lesson, student):
        """Create questions for Python File Handling lesson"""
        # Question 1: File Opening
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="File Opening",
            content="What is the correct way to open a file for reading in Python?",
            options=[
                "A) open('file.txt', 'r')",
                "B) open('file.txt', 'read')",
                "C) open('file.txt', 'w')",
                "D) open('file.txt')"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["files", "io"]
        )
        
        Hint.objects.create(question=q1, content="'r' mode opens a file for reading.", order_index=1, penalty_points=2)
        
        # Question 2: Exception Handling
        q2 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Exception Handling",
            content="What keyword is used to handle exceptions in Python?",
            options=[
                "A) try-except",
                "B) try-catch",
                "C) handle",
                "D) catch"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=2,
            tags=["exceptions", "error-handling"]
        )
        
        Hint.objects.create(question=q2, content="Python uses 'try-except' blocks for exception handling.", order_index=1, penalty_points=2)
        
        # Question 3: Coding Question
        q3 = Question.objects.create(
            lesson=lesson,
            question_type='coding',
            title="File Reading",
            content="Write a Python function that reads a file and returns its content as a string.",
            options=None,
            correct_answer=[{"test_cases": [
                {"input": "test.txt", "expected": "Hello World"},
                {"input": "empty.txt", "expected": ""}
            ]}],
            difficulty=3,
            points=20,
            order_index=3,
            tags=["files", "coding"]
        )
        
        Hint.objects.create(question=q3, content="Use open() with 'r' mode and read() method.", order_index=1, penalty_points=3)
        Hint.objects.create(question=q3, content="Don't forget to close the file or use 'with' statement.", order_index=2, penalty_points=4)

    def create_js_variables_questions(self, lesson, student):
        """Create questions for JavaScript Variables lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Variable Declaration",
            content="Which keyword is used to declare a variable that can be reassigned in JavaScript?",
            options=[
                "A) const",
                "B) let",
                "C) var",
                "D) Both B and C"
            ],
            correct_answer=["D"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["variables", "javascript"]
        )
        
        Hint.objects.create(question=q1, content="Both 'let' and 'var' allow reassignment, but 'const' does not.", order_index=1, penalty_points=2)

    def create_js_functions_questions(self, lesson, student):
        """Create questions for JavaScript Functions lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Function Declaration",
            content="Which of the following is NOT a way to create a function in JavaScript?",
            options=[
                "A) function myFunc() {}",
                "B) const myFunc = function() {}",
                "C) const myFunc = () => {}",
                "D) def myFunc() {}"
            ],
            correct_answer=["D"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["functions", "javascript"]
        )
        
        Hint.objects.create(question=q1, content="'def' is Python syntax, not JavaScript.", order_index=1, penalty_points=2)

    def create_js_arrays_questions(self, lesson, student):
        """Create questions for JavaScript Arrays lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Array Methods",
            content="Which method adds an element to the end of an array?",
            options=[
                "A) push()",
                "B) pop()",
                "C) shift()",
                "D) unshift()"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["arrays", "methods"]
        )
        
        Hint.objects.create(question=q1, content="push() adds to the end, pop() removes from the end.", order_index=1, penalty_points=2)

    def create_js_dom_questions(self, lesson, student):
        """Create questions for JavaScript DOM lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="DOM Selection",
            content="Which method selects the first element with a specific ID?",
            options=[
                "A) getElementById()",
                "B) getElementsByClassName()",
                "C) querySelector()",
                "D) Both A and C"
            ],
            correct_answer=["D"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["dom", "selection"]
        )
        
        Hint.objects.create(question=q1, content="Both methods can select by ID: getElementById('id') and querySelector('#id').", order_index=1, penalty_points=2)

    def create_html_questions(self, lesson, student):
        """Create questions for HTML lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="HTML Structure",
            content="What is the correct HTML5 document structure?",
            options=[
                "A) <html><head><body></body></head></html>",
                "B) <html><head></head><body></body></html>",
                "C) <head><html><body></body></html></head>",
                "D) <body><head></head><html></html></body>"
            ],
            correct_answer=["B"],
            difficulty=1,
            points=10,
            order_index=1,
            tags=["html", "structure"]
        )
        
        Hint.objects.create(question=q1, content="HTML structure should be: html > head + body", order_index=1, penalty_points=2)

    def create_css_questions(self, lesson, student):
        """Create questions for CSS lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="CSS Selectors",
            content="Which selector targets elements with a specific class?",
            options=[
                "A) #classname",
                "B) .classname",
                "C) classname",
                "D) *classname"
            ],
            correct_answer=["B"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["css", "selectors"]
        )
        
        Hint.objects.create(question=q1, content="Class selectors use a dot (.) prefix.", order_index=1, penalty_points=2)

    def create_js_events_questions(self, lesson, student):
        """Create questions for JavaScript Events lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Event Handling",
            content="Which method is used to add an event listener in JavaScript?",
            options=[
                "A) addEventListener()",
                "B) on()",
                "C) attachEvent()",
                "D) listen()"
            ],
            correct_answer=["A"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["events", "javascript"]
        )
        
        Hint.objects.create(question=q1, content="addEventListener() is the modern way to handle events.", order_index=1, penalty_points=2)

    def create_responsive_questions(self, lesson, student):
        """Create questions for Responsive Design lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Media Queries",
            content="What CSS feature is used to make designs responsive?",
            options=[
                "A) Media queries",
                "B) Flexbox",
                "C) Grid",
                "D) All of the above"
            ],
            correct_answer=["D"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["responsive", "css"]
        )
        
        Hint.objects.create(question=q1, content="Responsive design uses multiple CSS features together.", order_index=1, penalty_points=2)

    def create_api_questions(self, lesson, student):
        """Create questions for API Integration lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="HTTP Methods",
            content="Which HTTP method is used to retrieve data from an API?",
            options=[
                "A) POST",
                "B) GET",
                "C) PUT",
                "D) DELETE"
            ],
            correct_answer=["B"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["api", "http"]
        )
        
        Hint.objects.create(question=q1, content="GET is used for retrieving/reading data.", order_index=1, penalty_points=2)

    def create_numpy_questions(self, lesson, student):
        """Create questions for NumPy lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="NumPy Arrays",
            content="What is the main data structure in NumPy?",
            options=[
                "A) List",
                "B) Array",
                "C) ndarray",
                "D) Matrix"
            ],
            correct_answer=["C"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["numpy", "arrays"]
        )
        
        Hint.objects.create(question=q1, content="NumPy's main data structure is called ndarray (n-dimensional array).", order_index=1, penalty_points=2)

    def create_pandas_questions(self, lesson, student):
        """Create questions for Pandas lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Pandas DataFrames",
            content="What is the main data structure in Pandas?",
            options=[
                "A) Series",
                "B) DataFrame",
                "C) Array",
                "D) Both A and B"
            ],
            correct_answer=["D"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["pandas", "dataframes"]
        )
        
        Hint.objects.create(question=q1, content="Pandas has two main structures: Series (1D) and DataFrame (2D).", order_index=1, penalty_points=2)

    def create_visualization_questions(self, lesson, student):
        """Create questions for Data Visualization lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Matplotlib",
            content="Which Python library is commonly used for data visualization?",
            options=[
                "A) matplotlib",
                "B) seaborn",
                "C) plotly",
                "D) All of the above"
            ],
            correct_answer=["D"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["visualization", "matplotlib"]
        )
        
        Hint.objects.create(question=q1, content="All three are popular Python visualization libraries.", order_index=1, penalty_points=2)

    def create_statistics_questions(self, lesson, student):
        """Create questions for Statistical Analysis lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Central Tendency",
            content="Which measure represents the middle value in a dataset?",
            options=[
                "A) Mean",
                "B) Median",
                "C) Mode",
                "D) All of the above"
            ],
            correct_answer=["B"],
            difficulty=2,
            points=15,
            order_index=1,
            tags=["statistics", "central-tendency"]
        )
        
        Hint.objects.create(question=q1, content="Median is the middle value when data is sorted.", order_index=1, penalty_points=2)

    def create_linear_regression_questions(self, lesson, student):
        """Create questions for Linear Regression lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Linear Regression",
            content="What type of problem does linear regression solve?",
            options=[
                "A) Classification",
                "B) Regression",
                "C) Clustering",
                "D) Dimensionality reduction"
            ],
            correct_answer=["B"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["regression", "machine-learning"]
        )
        
        Hint.objects.create(question=q1, content="Linear regression predicts continuous numerical values.", order_index=1, penalty_points=2)

    def create_classification_questions(self, lesson, student):
        """Create questions for Classification lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Classification",
            content="What type of problem does classification solve?",
            options=[
                "A) Predicting continuous values",
                "B) Predicting categories/classes",
                "C) Finding patterns in data",
                "D) Reducing data dimensions"
            ],
            correct_answer=["B"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["classification", "machine-learning"]
        )
        
        Hint.objects.create(question=q1, content="Classification predicts discrete categories or classes.", order_index=1, penalty_points=2)

    def create_neural_networks_questions(self, lesson, student):
        """Create questions for Neural Networks lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Neural Networks",
            content="What is the basic building block of a neural network?",
            options=[
                "A) Layer",
                "B) Neuron",
                "C) Weight",
                "D) Bias"
            ],
            correct_answer=["B"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["neural-networks", "deep-learning"]
        )
        
        Hint.objects.create(question=q1, content="Neurons (or nodes) are the basic processing units in neural networks.", order_index=1, penalty_points=2)

    def create_model_evaluation_questions(self, lesson, student):
        """Create questions for Model Evaluation lesson"""
        q1 = Question.objects.create(
            lesson=lesson,
            question_type='mcq',
            title="Model Evaluation",
            content="What metric is used to evaluate classification models?",
            options=[
                "A) Accuracy",
                "B) RMSE",
                "C) R-squared",
                "D) All of the above"
            ],
            correct_answer=["A"],
            difficulty=3,
            points=20,
            order_index=1,
            tags=["evaluation", "metrics"]
        )
        
        Hint.objects.create(question=q1, content="Accuracy measures correct predictions in classification.", order_index=1, penalty_points=2)
