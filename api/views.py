from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import Student, Course, Lesson, Attempt, Question, Hint, QuestionAttempt
from .serializers import (
    StudentSerializer, CourseSerializer, LessonSerializer, AttemptSerializer,
    QuestionSerializer, HintSerializer, QuestionAttemptSerializer
)
from .services.recommender import get_recommendation

# Custom throttling classes - Disabled for development
class StrictAnonRateThrottle:
    """Disabled throttling for development"""
    def allow_request(self, request, view):
        return True

class StrictUserRateThrottle:
    """Disabled throttling for development"""
    def allow_request(self, request, view):
        return True

# Generic views for courses and lessons
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    throttle_classes = []  # Explicitly disable throttling

class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer
    throttle_classes = []  # Explicitly disable throttling

    def get_queryset(self):
        queryset = Lesson.objects.select_related('course').all()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

# Student Overview
class StudentOverview(APIView):
    throttle_classes = []  # Explicitly disable throttling

    def get(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Optimize queries with select_related and prefetch_related
        courses = Course.objects.prefetch_related('lessons').all()
        student_attempts = Attempt.objects.filter(student=student).select_related('lesson__course')

        # Create course lookup for IDs
        course_lookup = {course.name: course.id for course in courses}

        # Create lookup dictionaries to avoid N+1 queries
        attempt_counts = {}
        last_activities = {}
        attempted_lesson_ids = set()

        for attempt in student_attempts:
            course_id = attempt.lesson.course.id
            lesson_id = attempt.lesson.id

            # Count attempts per course
            attempt_counts[course_id] = attempt_counts.get(course_id, 0) + 1

            # Track last activity per course
            if course_id not in last_activities or attempt.timestamp > last_activities[course_id]:
                last_activities[course_id] = attempt.timestamp

            # Track attempted lessons
            attempted_lesson_ids.add(lesson_id)

        data = []
        for course in courses:
            lessons = list(course.lessons.order_by('order_index'))
            lesson_count = len(lessons)

            # Find next unattempted lesson
            next_up = None
            for lesson in lessons:
                if lesson.id not in attempted_lesson_ids:
                    next_up = lesson
                    break

            data.append({
                "course_id": course.id,
                "course_name": course.name,
                "progress": attempt_counts.get(course.id, 0) / lesson_count if lesson_count > 0 else 0,
                "last_activity": last_activities.get(course.id),
                "next_up": next_up.title if next_up else None
            })

        return Response(data)

# Recommendation Endpoint
class StudentRecommendation(APIView):
    throttle_classes = []  # Explicitly disable throttling

    def get(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        recommendation = get_recommendation(student)
        return Response(recommendation)

# Create Attempt
class AttemptCreate(generics.CreateAPIView):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    throttle_classes = []  # Explicitly disable throttling

# Analyze JavaScript Code (static analysis rules)
class AnalyzeCode(APIView):
    throttle_classes = []  # Explicitly disable throttling

    def post(self, request):
        code = request.data.get("code", "")

        if not code.strip():
            return Response({"error": "Code cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        issues = self.analyze_javascript(code)
        return Response({"issues": issues})

    def analyze_javascript(self, code):
        """AST-based JavaScript static analysis"""
        issues = []
        
        try:
            # For now, we'll keep the existing JavaScript analysis
            # In a real implementation, you'd use a JavaScript parser like esprima
            # or call the frontend analyzer via API
            lines = code.split('\n')

            for i, line in enumerate(lines, 1):
                # Check for unused variables (simple heuristic)
                if 'var ' in line or 'let ' in line or 'const ' in line:
                    var_match = line.split('var ')[-1] if 'var ' in line else line
                    var_match = var_match.split('let ')[-1] if 'let ' in var_match else var_match
                    var_match = var_match.split('const ')[-1] if 'const ' in var_match else var_match
                    var_name = var_match.split('=')[0].split(';')[0].strip()

                    # Simple check if variable is used elsewhere (basic)
                    var_used = any(var_name in other_line and f'{var_name}(' not in other_line
                                 for j, other_line in enumerate(lines) if j != i-1)

                    if not var_used and len(var_name) > 1:
                        issues.append({
                            "type": "unused_variable",
                            "line": i,
                            "message": f"Variable '{var_name}' is declared but never used",
                            "suggestion": "Remove the unused variable or use it in your code"
                        })

                # Check for off-by-one errors in loops
                if 'for ' in line and ('length' in line or 'Length' in line):
                    if '<=' in line and 'length' in line:
                        issues.append({
                            "type": "potential_off_by_one",
                            "line": i,
                            "message": "Potential off-by-one error in loop condition",
                            "suggestion": "Check if you should use '<' instead of '<=' or vice versa"
                        })

                # Check for missing return in functions
                if ('function ' in line or '=> ' in line) and '{' in line:
                    # Simple check for functions that should return but don't
                    func_end_line = i
                    brace_count = line.count('{') - line.count('}')
                    for j in range(i, min(i+10, len(lines))):  # Check next 10 lines
                        func_end_line = j
                        brace_count += lines[j].count('{') - lines[j].count('}')
                        if brace_count <= 0:
                            break

                    func_body = '\n'.join(lines[i:func_end_line+1])
                    if ('return ' not in func_body and
                        '=>' not in line and  # Arrow functions might not need return
                        'console.log' not in func_body):  # Simple functions might not need return
                        issues.append({
                            "type": "missing_return",
                            "line": i,
                            "message": "Function may be missing a return statement",
                            "suggestion": "Add a return statement or check if this function should return a value"
                        })

        except Exception as e:
            issues.append({
                "type": "parse_error",
                "line": 1,
                "message": f"Failed to analyze code: {str(e)}",
                "suggestion": "Check for syntax errors in your code"
            })

        return issues


# Question Management
class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    throttle_classes = []  # Explicitly disable throttling

    def get_queryset(self):
        queryset = Question.objects.select_related('lesson__course').prefetch_related('hints').all()
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.select_related('lesson__course').prefetch_related('hints')
    serializer_class = QuestionSerializer
    throttle_classes = []  # Explicitly disable throttling


class QuestionAttemptCreate(generics.CreateAPIView):
    queryset = QuestionAttempt.objects.all()
    serializer_class = QuestionAttemptSerializer
    throttle_classes = []  # Explicitly disable throttling

    def perform_create(self, serializer):
        """Automatically calculate points earned based on correctness and hints used"""
        question_attempt = serializer.save()

        # Calculate points earned
        question = question_attempt.question
        base_points = question.points
        hint_penalty = sum(
            hint.penalty_points
            for hint in question.hints.all()[:question_attempt.hints_used]
        )

        points_earned = max(0, base_points - hint_penalty) if question_attempt.is_correct else 0
        question_attempt.points_earned = points_earned
        question_attempt.save()


class StudentQuestionAttempts(APIView):
    throttle_classes = []  # Explicitly disable throttling

    def get(self, request, pk):
        """Get all question attempts for a student"""
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        attempts = QuestionAttempt.objects.filter(
            student=student
        ).select_related('question__lesson__course').order_by('-timestamp')

        serializer = QuestionAttemptSerializer(attempts, many=True)
        return Response(serializer.data)


class LessonQuestions(APIView):
    throttle_classes = []  # Explicitly disable throttling

    def get(self, request, lesson_id):
        """Get all questions for a lesson with student's progress"""
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get questions for this lesson
        questions = Question.objects.filter(
            lesson=lesson
        ).prefetch_related('hints').order_by('order_index')

        # Get student ID from query params
        student_id = request.query_params.get('student')
        question_data = []

        for question in questions:
            question_info = QuestionSerializer(question).data

            # Add progress info if student is specified
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    latest_attempt = QuestionAttempt.objects.filter(
                        student=student,
                        question=question
                    ).order_by('-timestamp').first()

                    if latest_attempt:
                        question_info['attempted'] = True
                        question_info['last_attempt'] = {
                            'is_correct': latest_attempt.is_correct,
                            'hints_used': latest_attempt.hints_used,
                            'points_earned': latest_attempt.points_earned,
                            'timestamp': latest_attempt.timestamp
                        }
                    else:
                        question_info['attempted'] = False
                        question_info['last_attempt'] = None
                except Student.DoesNotExist:
                    question_info['attempted'] = False
                    question_info['last_attempt'] = None
            else:
                question_info['attempted'] = False
                question_info['last_attempt'] = None

            question_data.append(question_info)

        return Response({
            'lesson': {
                'id': lesson.id,
                'title': lesson.title,
                'course_name': lesson.course.name
            },
            'questions': question_data
        })
