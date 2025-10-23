from django.urls import path
from .views import StudentOverview, StudentRecommendation, AttemptCreate, AnalyzeCode

urlpatterns = [
    path('students/<int:pk>/overview/', StudentOverview.as_view()),
    path('students/<int:pk>/recommendation/', StudentRecommendation.as_view()),
    path('attempts/', AttemptCreate.as_view()),
    path('analyze-code/', AnalyzeCode.as_view()),
]
