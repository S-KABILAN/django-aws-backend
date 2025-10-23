from django.core.management.base import BaseCommand
from api.models import Student, Course, Lesson, Attempt
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **options):
        student = Student.objects.create(name="Demo Student", email="demo@student.com")
        course = Course.objects.create(name="Python 101", description="Learn Python", difficulty=2)
        lesson1 = Lesson.objects.create(course=course, title="Intro", tags=["python"], order_index=1)
        lesson2 = Lesson.objects.create(course=course, title="Loops", tags=["python", "loops"], order_index=2)
        Attempt.objects.create(student=student, lesson=lesson1, correctness=0.8, hints_used=1, duration_sec=300)
        self.stdout.write(self.style.SUCCESS("Demo data created"))
