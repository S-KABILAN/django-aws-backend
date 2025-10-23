import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Student, Course, Lesson, Attempt


@pytest.mark.django_db
class TestModels:
    def test_student_creation(self):
        student = Student.objects.create(name="Test Student", email="test@example.com")
        assert student.name == "Test Student"
        assert student.email == "test@example.com"
        assert str(student) == "Test Student"

    def test_course_creation(self):
        course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            difficulty=2
        )
        assert course.name == "Test Course"
        assert course.difficulty == 2
        assert str(course) == "Test Course"

    def test_lesson_creation(self):
        course = Course.objects.create(name="Test Course", description="Test", difficulty=1)
        lesson = Lesson.objects.create(
            course=course,
            title="Test Lesson",
            tags=["tag1", "tag2"],
            order_index=1
        )
        assert lesson.title == "Test Lesson"
        assert lesson.order_index == 1
        assert str(lesson) == "Test Course - Test Lesson"

    def test_attempt_creation(self):
        course = Course.objects.create(name="Test Course", description="Test", difficulty=1)
        lesson = Lesson.objects.create(course=course, title="Test Lesson", tags=[], order_index=1)
        student = Student.objects.create(name="Test Student", email="test@example.com")

        attempt = Attempt.objects.create(
            student=student,
            lesson=lesson,
            correctness=0.85,
            hints_used=1,
            duration_sec=300
        )
        assert attempt.correctness == 0.85
        assert attempt.hints_used == 1


@pytest.mark.django_db
class TestAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def sample_data(self):
        student = Student.objects.create(name="Test Student", email="test@example.com")
        course = Course.objects.create(name="Python 101", description="Learn Python", difficulty=2)
        lesson1 = Lesson.objects.create(course=course, title="Variables", tags=["python"], order_index=1)
        lesson2 = Lesson.objects.create(course=course, title="Loops", tags=["python"], order_index=2)
        Attempt.objects.create(student=student, lesson=lesson1, correctness=0.8, hints_used=1, duration_sec=300)
        return student, course, lesson1, lesson2

    def test_student_overview_success(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('student-overview', kwargs={'pk': student.id})
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['course_name'] == 'Python 101'
        assert 'progress' in response.data[0]
        assert 'last_activity' in response.data[0]
        assert 'next_up' in response.data[0]

    def test_student_overview_not_found(self, client):
        url = reverse('student-overview', kwargs={'pk': 999})
        response = client.get(url)

        assert response.status_code == 404
        assert 'error' in response.data

    def test_student_recommendation_success(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('student-recommendation', kwargs={'pk': student.id})
        response = client.get(url)

        assert response.status_code == 200
        assert 'recommendation' in response.data
        assert 'confidence' in response.data
        assert 'reason_features' in response.data
        assert 'alternatives' in response.data
        assert 0 <= response.data['confidence'] <= 1

    def test_student_recommendation_not_found(self, client):
        url = reverse('student-recommendation', kwargs={'pk': 999})
        response = client.get(url)

        assert response.status_code == 404
        assert 'error' in response.data

    def test_create_attempt_success(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('attempt-create')
        data = {
            'student': student.id,
            'lesson': lesson1.id,
            'correctness': 0.9,
            'hints_used': 2,
            'duration_sec': 250
        }
        response = client.post(url, data, format='json')

        assert response.status_code == 201
        assert response.data['correctness'] == 0.9
        assert response.data['hints_used'] == 2

    def test_create_attempt_validation_error(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('attempt-create')

        # Test invalid correctness
        data = {
            'student': student.id,
            'lesson': lesson1.id,
            'correctness': 1.5,  # Invalid: > 1
            'hints_used': 2,
            'duration_sec': 250
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400

        # Test negative hints_used
        data['correctness'] = 0.8
        data['hints_used'] = -1
        response = client.post(url, data, format='json')
        assert response.status_code == 400

        # Test negative duration
        data['hints_used'] = 1
        data['duration_sec'] = -100
        response = client.post(url, data, format='json')
        assert response.status_code == 400

    def test_code_analysis_success(self, client):
        url = reverse('analyze-code')
        data = {'code': 'function test() { return "hello"; }'}
        response = client.post(url, data, format='json')

        assert response.status_code == 200
        assert 'issues' in response.data
        assert isinstance(response.data['issues'], list)

    def test_code_analysis_empty_code(self, client):
        url = reverse('analyze-code')
        data = {'code': ''}
        response = client.post(url, data, format='json')

        assert response.status_code == 400
        assert 'error' in response.data

    def test_courses_list(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('course-list')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Python 101'

    def test_lessons_list(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = reverse('lesson-list')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['title'] in ['Variables', 'Loops']
        assert response.data[1]['title'] in ['Variables', 'Loops']

    def test_lessons_filtered_by_course(self, client, sample_data):
        student, course, lesson1, lesson2 = sample_data
        url = f"{reverse('lesson-list')}?course={course.id}"
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert all(lesson['course'] == course.id for lesson in response.data)


@pytest.mark.django_db
class TestRecommenderDeterminism:
    @pytest.fixture
    def sample_data(self):
        student = Student.objects.create(name="Test Student", email="test@example.com")
        course = Course.objects.create(name="Test Course", description="Test", difficulty=2)

        # Create multiple lessons
        lessons = []
        for i in range(5):
            lesson = Lesson.objects.create(
                course=course,
                title=f"Lesson {i+1}",
                tags=["tag"],
                order_index=i+1
            )
            lessons.append(lesson)

        # Create attempts with varying timestamps and performance
        base_time = 1638360000000  # 2021-12-01 in milliseconds
        for i, lesson in enumerate(lessons[:3]):  # Only first 3 lessons have attempts
            Attempt.objects.create(
                student=student,
                lesson=lesson,
                timestamp=f"2021-12-{i+1:02d}T10:00:00Z",
                correctness=0.5 + i * 0.2,  # 0.5, 0.7, 0.9
                hints_used=i,
                duration_sec=200 + i * 50
            )

        return student, lessons

    def test_recommender_determinism(self, sample_data):
        """Test that recommender gives consistent results for same input"""
        student, lessons = sample_data

        # Make multiple calls to ensure determinism
        results = []
        for _ in range(3):
            from .services.recommender import get_recommendation
            result = get_recommendation(student)
            results.append(result)

        # All results should be identical
        for i in range(1, len(results)):
            assert results[0]['recommendation'] == results[i]['recommendation']
            assert results[0]['confidence'] == results[i]['confidence']
            assert len(results[0]['alternatives']) == len(results[i]['alternatives'])

    def test_recommender_features_completeness(self, sample_data):
        """Test that all expected features are calculated"""
        student, lessons = sample_data

        from .services.recommender import get_recommendation
        result = get_recommendation(student)

        features = result['reason_features']
        expected_features = [
            'time_since_last_activity', 'avg_correctness_7d', 'avg_correctness_30d',
            'progress_gap', 'tag_mastery_gap', 'hints_rate', 'difficulty_drift',
            'attempts_to_completion_ratio'
        ]

        for feature in expected_features:
            assert feature in features, f"Missing feature: {feature}"

    def test_recommender_confidence_range(self, sample_data):
        """Test that confidence is always between 0 and 1"""
        student, lessons = sample_data

        from .services.recommender import get_recommendation
        result = get_recommendation(student)

        assert 0 <= result['confidence'] <= 1, f"Confidence {result['confidence']} out of range"

        for alt in result['alternatives']:
            assert 0 <= alt['confidence'] <= 1, f"Alternative confidence {alt['confidence']} out of range"

    def test_recommender_alternatives(self, sample_data):
        """Test that alternatives are properly generated"""
        student, lessons = sample_data

        from .services.recommender import get_recommendation
        result = get_recommendation(student)

        assert 'alternatives' in result
        assert isinstance(result['alternatives'], list)
        assert len(result['alternatives']) <= 2  # Max 2 alternatives

        for alt in result['alternatives']:
            assert 'lesson' in alt
            assert 'confidence' in alt
            assert isinstance(alt['lesson'], str)
            assert isinstance(alt['confidence'], (int, float))
