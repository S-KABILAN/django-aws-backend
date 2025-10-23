from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student, Course, Lesson, Attempt
from .serializers import StudentSerializer, CourseSerializer, LessonSerializer, AttemptSerializer
from .services.recommender import get_recommendation

# Student Overview
class StudentOverview(APIView):
    def get(self, request, pk):
        student = Student.objects.get(id=pk)
        courses = Course.objects.all()  # can filter enrolled courses later
        data = []
        for course in courses:
            lessons = course.lessons.order_by('order_index')
            last_activity = Attempt.objects.filter(student=student, lesson__course=course).order_by('-timestamp').first()
            progress = Attempt.objects.filter(student=student, lesson__course=course).count() / lessons.count()
            next_up = lessons.exclude(id__in=Attempt.objects.filter(student=student, lesson__course=course).values_list('lesson_id', flat=True)).first()
            data.append({
                "course_name": course.name,
                "progress": progress,
                "last_activity": last_activity.timestamp if last_activity else None,
                "next_up": next_up.title if next_up else None
            })
        return Response(data)

# Recommendation Endpoint
class StudentRecommendation(APIView):
    def get(self, request, pk):
        student = Student.objects.get(id=pk)
        recommendation = get_recommendation(student)
        return Response(recommendation)

# Create Attempt
class AttemptCreate(generics.CreateAPIView):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer

# Analyze Python Code (basic AST rules)
class AnalyzeCode(APIView):
    def post(self, request):
        code = request.data.get("code", "")
        issues = []  # add AST static rules here
        return Response({"issues": issues})
