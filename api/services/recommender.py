from datetime import datetime, timedelta
from ..models import Lesson, Attempt
import random

def get_recommendation(student):
    """
    Returns a deterministic recommendation for a student with:
    - lesson/course to do next
    - reason features
    - confidence [0..1]
    - top 2 alternatives
    """

    # Deterministic randomness based on student id
    random.seed(student.id)

    # Get all lessons
    lessons = Lesson.objects.all()
    recommendations = []

    now = datetime.now()

    for lesson in lessons:
        attempts = Attempt.objects.filter(student=student, lesson=lesson).order_by('-timestamp')

        # Feature 1: time since last activity (days)
        if attempts.exists():
            last_attempt = attempts.first()
            time_since_last_activity = (now - last_attempt.timestamp).days
            avg_correctness_7d = attempts.filter(timestamp__gte=now - timedelta(days=7)).aggregate(avg=models.Avg('correctness'))['avg'] or 0
            avg_correctness_30d = attempts.filter(timestamp__gte=now - timedelta(days=30)).aggregate(avg=models.Avg('correctness'))['avg'] or 0
            attempts_to_completion_ratio = len(attempts) / max(1, lesson.order_index)
            hints_rate = sum([a.hints_used for a in attempts]) / max(1, len(attempts))
        else:
            time_since_last_activity = 999
            avg_correctness_7d = 0
            avg_correctness_30d = 0
            attempts_to_completion_ratio = 0
            hints_rate = 0

        # Feature 2: progress gap (0=complete, 1=not started)
        progress_gap = 1 if not attempts.exists() else 1 - attempts_to_completion_ratio

        # Feature 3: tag mastery gap (simplified: assume 0.5 if attempted)
        tag_mastery_gap = 0.5 if attempts.exists() else 1.0

        # Feature 4: difficulty drift (assuming course difficulty - correctness)
        difficulty_drift = (lesson.course.difficulty / 5) - (avg_correctness_30d)

        # Weighted scoring
        score = (
            0.2 * min(time_since_last_activity/30,1) +
            0.2 * progress_gap +
            0.2 * tag_mastery_gap +
            0.2 * (1 - avg_correctness_7d) +
            0.2 * difficulty_drift
        )

        # Confidence is normalized [0..1]
        confidence = max(0, min(1, 1 - score + random.uniform(-0.05, 0.05)))

        # Collect recommendation
        recommendations.append({
            "lesson": lesson.title,
            "features": {
                "time_since_last_activity": time_since_last_activity,
                "avg_correctness_7d": avg_correctness_7d,
                "avg_correctness_30d": avg_correctness_30d,
                "progress_gap": progress_gap,
                "tag_mastery_gap": tag_mastery_gap,
                "hints_rate": hints_rate,
                "difficulty_drift": difficulty_drift,
                "attempts_to_completion_ratio": attempts_to_completion_ratio
            },
            "confidence": confidence
        })

    # Sort by confidence descending
    recommendations.sort(key=lambda x: x["confidence"], reverse=True)

    # Main recommendation
    top = recommendations[0] if recommendations else None

    # Top 2 alternatives
    alternatives = recommendations[1:3] if len(recommendations) > 1 else []

    return {
        "recommendation": top["lesson"] if top else None,
        "reason_features": top["features"] if top else {},
        "confidence": top["confidence"] if top else 0,
        "alternatives": alternatives
    }
