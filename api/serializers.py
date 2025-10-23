from rest_framework import serializers
from .models import Student, Course, Lesson, Attempt, Question, Hint, QuestionAttempt

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = "__all__"

    def validate_correctness(self, value):
        """Validate correctness is between 0 and 1"""
        if not (0 <= value <= 1):
            raise serializers.ValidationError("Correctness must be between 0 and 1")
        return value

    def validate_hints_used(self, value):
        """Validate hints_used is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Hints used cannot be negative")
        return value

    def validate_duration_sec(self, value):
        """Validate duration is positive"""
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    hints = HintSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"

    def validate_difficulty(self, value):
        """Validate difficulty is between 1 and 5"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Difficulty must be between 1 and 5")
        return value

    def validate_points(self, value):
        """Validate points is positive"""
        if value <= 0:
            raise serializers.ValidationError("Points must be positive")
        return value


class QuestionAttemptSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question.title', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)

    class Meta:
        model = QuestionAttempt
        fields = "__all__"

    def validate_hints_used(self, value):
        """Validate hints_used is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Hints used cannot be negative")
        return value

    def validate_duration_sec(self, value):
        """Validate duration is positive"""
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value

    def validate_points_earned(self, value):
        """Validate points earned is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Points earned cannot be negative")
        return value