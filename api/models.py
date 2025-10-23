from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.IntegerField()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=100)
    tags = models.JSONField()
    order_index = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} - {self.title}"

class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attempts")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attempts")
    timestamp = models.DateTimeField(auto_now_add=True)
    correctness = models.FloatField()
    hints_used = models.IntegerField()
    duration_sec = models.IntegerField()
