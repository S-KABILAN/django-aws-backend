from django.urls import path
from .views import (
    StudentOverview, StudentRecommendation, AttemptCreate, AnalyzeCode,
    CourseList, LessonList, QuestionList, QuestionDetail, QuestionAttemptCreate,
    StudentQuestionAttempts, LessonQuestions
)

urlpatterns = [
    path('students/<int:pk>/overview/', StudentOverview.as_view(), name='student-overview'),
    path('students/<int:pk>/recommendation/', StudentRecommendation.as_view(), name='student-recommendation'),
    path('students/<int:pk>/question-attempts/', StudentQuestionAttempts.as_view(), name='student-question-attempts'),
    path('courses/', CourseList.as_view(), name='course-list'),
    path('lessons/', LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:lesson_id>/questions/', LessonQuestions.as_view(), name='lesson-questions'),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('question-attempts/', QuestionAttemptCreate.as_view(), name='question-attempt-create'),
    path('attempts/', AttemptCreate.as_view(), name='attempt-create'),
    path('analyze-code/', AnalyzeCode.as_view(), name='analyze-code'),
]
