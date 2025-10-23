from django.urls import path
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Hello, world!"})

urlpatterns = [
    path("", home),
]
