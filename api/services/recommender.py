from datetime import timedelta
from ..models import Lesson, Attempt, Question, QuestionAttempt
from django.utils import timezone
from django.db import models

def get_recommendation(student):
    """
    Returns a deterministic recommendation for a student with:
    - lesson/course to do next
    - reason features
    - confidence [0..1]
    - top 2 alternatives
    """

    # No longer using random numbers - confidence is now data-driven

    # Get all lessons
    lessons = Lesson.objects.all()
    recommendations = []

    now = timezone.now()  # Use timezone-aware datetime

    for lesson in lessons:
        attempts = Attempt.objects.filter(student=student, lesson=lesson).order_by('-timestamp')

        # Get question attempts for this lesson
        question_attempts = QuestionAttempt.objects.filter(
            student=student,
            question__lesson=lesson
        ).select_related('question').order_by('-timestamp')

        # Feature 1: time since last activity (days) - consider both lesson and question attempts
        last_lesson_time = None
        last_question_time = None

        if attempts.exists():
            last_attempt = attempts.first()
            last_lesson_time = last_attempt.timestamp
            if timezone.is_naive(last_lesson_time):
                last_lesson_time = timezone.make_aware(last_lesson_time, timezone.get_current_timezone())

        if question_attempts.exists():
            last_question_attempt = question_attempts.first()
            last_question_time = last_question_attempt.timestamp
            if timezone.is_naive(last_question_time):
                last_question_time = timezone.make_aware(last_question_time, timezone.get_current_timezone())

        # Use the most recent activity
        last_activity_time = None
        if last_lesson_time and last_question_time:
            last_activity_time = max(last_lesson_time, last_question_time)
        elif last_lesson_time:
            last_activity_time = last_lesson_time
        elif last_question_time:
            last_activity_time = last_question_time

        if last_activity_time:
            time_since_last_activity = (now - last_activity_time).days
        else:
            time_since_last_activity = 999

        # Question-based performance metrics
        if question_attempts.exists():
            # Recent question performance
            avg_correctness_7d = question_attempts.filter(
                timestamp__gte=now - timedelta(days=7)
            ).aggregate(avg=models.Avg('is_correct'))['avg'] or 0

            avg_correctness_30d = question_attempts.filter(
                timestamp__gte=now - timedelta(days=30)
            ).aggregate(avg=models.Avg('is_correct'))['avg'] or 0

            # Hint usage patterns
            avg_hints_used = question_attempts.aggregate(avg=models.Avg('hints_used'))['avg'] or 0
            hint_usage_rate = min(avg_hints_used / 3, 1)  # Normalize hint usage (assuming max 3 hints per question)

            # Points earned ratio
            total_questions = Question.objects.filter(lesson=lesson).count()
            total_possible_points = Question.objects.filter(lesson=lesson).aggregate(
                total=models.Sum('points')
            )['total'] or 0
            total_earned_points = question_attempts.aggregate(
                total=models.Sum('points_earned')
            )['total'] or 0
            points_ratio = total_earned_points / max(total_possible_points, 1)

            # Question completion ratio
            unique_questions_attempted = question_attempts.values('question').distinct().count()
            question_completion_ratio = unique_questions_attempted / max(total_questions, 1)
        else:
            avg_correctness_7d = 0
            avg_correctness_30d = 0
            hint_usage_rate = 0
            points_ratio = 0
            question_completion_ratio = 0

        # Legacy lesson-based metrics (for backward compatibility)
        if attempts.exists():
            attempts_to_completion_ratio = len(attempts) / max(1, lesson.order_index)
            legacy_hints_rate = sum([a.hints_used for a in attempts]) / max(1, len(attempts))
            legacy_correctness_7d = attempts.filter(
                timestamp__gte=now - timedelta(days=7)
            ).aggregate(avg=models.Avg('correctness'))['avg'] or 0
            legacy_correctness_30d = attempts.filter(
                timestamp__gte=now - timedelta(days=30)
            ).aggregate(avg=models.Avg('correctness'))['avg'] or 0
        else:
            attempts_to_completion_ratio = 0
            legacy_hints_rate = 0
            legacy_correctness_7d = 0
            legacy_correctness_30d = 0

        # Combine metrics - prioritize question-based metrics when available
        if question_attempts.exists():
            combined_correctness_7d = avg_correctness_7d
            combined_correctness_30d = avg_correctness_30d
            combined_hints_rate = hint_usage_rate
        else:
            combined_correctness_7d = legacy_correctness_7d
            combined_correctness_30d = legacy_correctness_30d
            combined_hints_rate = legacy_hints_rate

        # Feature 2: progress gap (consider both lesson and question completion)
        has_lesson_attempts = attempts.exists()
        has_question_attempts = question_attempts.exists()
        combined_progress = (attempts_to_completion_ratio + question_completion_ratio) / 2
        progress_gap = 1 if not (has_lesson_attempts or has_question_attempts) else 1 - combined_progress

        # Feature 3: tag mastery gap (simplified)
        tag_mastery_gap = 0.5 if (has_lesson_attempts or has_question_attempts) else 1.0

        # Feature 4: difficulty drift (consider points earned as performance indicator)
        course_difficulty = lesson.course.difficulty / 5
        if question_attempts.exists():
            performance_indicator = points_ratio  # Use points ratio as performance indicator
        else:
            performance_indicator = combined_correctness_30d
        difficulty_drift = course_difficulty - performance_indicator

        # Feature 5: hint dependency (new feature)
        hint_dependency = combined_hints_rate  # Higher values indicate more hint usage

        # Weighted scoring - heavily prioritize lessons with recent activity
        # Lower score = higher priority (better recommendation)
        
        # Boost lessons with recent attempts (much higher priority)
        recent_activity_boost = 0
        if question_attempts.exists():
            recent_attempts = question_attempts.filter(
                timestamp__gte=now - timedelta(days=7)
            ).count()
            recent_activity_boost = min(recent_attempts * 0.3, 1.0)  # Up to 30% boost for recent activity
        
        score = (
            0.25 * min(time_since_last_activity/30, 1) +  # Recency (higher weight)
            0.15 * progress_gap +                           # Completion gap
            0.10 * tag_mastery_gap +                       # Concept mastery
            0.15 * (1 - combined_correctness_7d) +        # Recent performance gap
            0.10 * max(0, difficulty_drift) +              # Difficulty alignment
            0.15 * hint_dependency +                       # Hint usage (higher = more help needed)
            0.10 * (1 - question_completion_ratio)        # Question completion (prioritize incomplete lessons)
        ) - recent_activity_boost  # Subtract boost to lower score (better recommendation)

        # Confidence is based on recent activity and data freshness
        # Make confidence more responsive to recent attempts
        
        # Recent activity factor (most important for confidence)
        recent_activity_factor = 0
        if question_attempts.exists():
            # Count attempts in last 7 days
            recent_attempts_7d = question_attempts.filter(
                timestamp__gte=now - timedelta(days=7)
            ).count()
            # Count attempts in last 3 days (even more recent)
            recent_attempts_3d = question_attempts.filter(
                timestamp__gte=now - timedelta(days=3)
            ).count()
            
            # More gradual confidence boost - each attempt adds less
            recent_activity_factor = min(0.25, recent_attempts_3d * 0.05 + recent_attempts_7d * 0.02)
        
        # Data freshness factor
        data_freshness_factor = 0
        if last_activity_time:
            days_since_activity = (now - last_activity_time).days
            if days_since_activity <= 1:
                data_freshness_factor = 0.15  # Very fresh data
            elif days_since_activity <= 3:
                data_freshness_factor = 0.10  # Fresh data
            elif days_since_activity <= 7:
                data_freshness_factor = 0.05  # Recent data
            else:
                data_freshness_factor = 0.02  # Stale data
        
        # Performance factor (based on recent performance)
        performance_factor = 0
        if question_attempts.exists():
            recent_performance = combined_correctness_7d
            performance_factor = recent_performance * 0.2
        
        # Base confidence starts lower and builds up with activity
        base_confidence = 0.3  # Start with lower base confidence
        
        # Calculate dynamic confidence
        confidence = max(0.1, min(0.95, 
            base_confidence + 
            recent_activity_factor + 
            data_freshness_factor + 
            performance_factor
        ))
        
        # Add small variation based on lesson to make it more dynamic
        lesson_variation = (lesson.id % 7) * 0.02  # Small variation based on lesson ID
        confidence = max(0.1, min(0.95, confidence + lesson_variation))

        # Collect recommendation
        recommendations.append({
            "lesson": lesson.title,
            "features": {
                "time_since_last_activity": time_since_last_activity,
                "avg_correctness_7d": combined_correctness_7d,
                "avg_correctness_30d": combined_correctness_30d,
                "progress_gap": progress_gap,
                "tag_mastery_gap": tag_mastery_gap,
                "hints_rate": combined_hints_rate,
                "hint_dependency": hint_dependency,
                "difficulty_drift": difficulty_drift,
                "question_completion_ratio": question_completion_ratio,
                "points_ratio": points_ratio,
                "attempts_to_completion_ratio": attempts_to_completion_ratio
            },
            "confidence": confidence
        })

    # Sort by confidence descending
    recommendations.sort(key=lambda x: x["confidence"], reverse=True)

    top = recommendations[0] if recommendations else None
    alternatives = recommendations[1:3] if len(recommendations) > 1 else []

    return {
        "recommendation": top["lesson"] if top else None,
        "reason_features": top["features"] if top else {},
        "confidence": top["confidence"] if top else 0,
        "alternatives": alternatives
    }
