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

    class Meta:
        indexes = [
            models.Index(fields=['course', 'order_index']),
        ]

class Question(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice Question'),
        ('coding', 'Coding Problem'),
        ('text', 'Text Input'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    title = models.CharField(max_length=200)
    content = models.TextField()  # The question text
    options = models.JSONField(null=True, blank=True)  # For MCQ: ["A) Option 1", "B) Option 2", ...]
    correct_answer = models.JSONField()  # For MCQ: ["A"], for coding: could be test cases, for text: expected answer
    difficulty = models.IntegerField(default=1)  # 1-5 scale
    points = models.IntegerField(default=10)
    order_index = models.IntegerField()
    tags = models.JSONField(default=list)

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

    class Meta:
        indexes = [
            models.Index(fields=['lesson', 'order_index']),
        ]
        ordering = ['order_index']


class Hint(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="hints")
    content = models.TextField()
    order_index = models.IntegerField()  # Hints are revealed progressively
    penalty_points = models.IntegerField(default=2)  # Points deducted for using this hint

    def __str__(self):
        return f"Hint {self.order_index} for {self.question.title}"

    class Meta:
        ordering = ['order_index']


class QuestionAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="question_attempts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempts")
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.JSONField()  # Student's answer
    is_correct = models.BooleanField()
    hints_used = models.IntegerField(default=0)  # Number of hints revealed
    duration_sec = models.IntegerField()
    points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.name} - {self.question.title} ({'✓' if self.is_correct else '✗'})"

    class Meta:
        indexes = [
            models.Index(fields=['student', 'timestamp']),
            models.Index(fields=['question', 'timestamp']),
            models.Index(fields=['student', 'question']),  # For finding latest attempts
        ]


class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attempts")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attempts")
    timestamp = models.DateTimeField(auto_now_add=True)
    correctness = models.FloatField()
    hints_used = models.IntegerField()
    duration_sec = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['student', 'timestamp']),
            models.Index(fields=['lesson', 'timestamp']),
        ]