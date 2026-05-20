from django.utils import timezone
from django.db.models import Count, Q
from .models import ScanSession
from apps.accounts.models import CustomUser
from apps.policies.models import FeedbackReport


class SystemStatistics:

    @staticmethod
    def get_daily_stats():
        today = timezone.now().date()
        scans = ScanSession.objects.filter(created_at__date=today)

        total      = scans.count()
        genuine    = scans.filter(result='genuine').count()
        counterfeit = scans.filter(result='counterfeit').count()

        return {
            "date":              str(today),
            "total_scans":       total,
            "genuine_count":     genuine,
            "counterfeit_count": counterfeit,
            "counterfeit_rate":  round((counterfeit / total * 100), 2) if total > 0 else 0,
        }

    @staticmethod
    def get_users_stats():
        return {
            "total_users":   CustomUser.objects.count(),
            "guests":        CustomUser.objects.filter(role='guest').count(),
            "regular_users": CustomUser.objects.filter(role='user').count(),
            "experts":       CustomUser.objects.filter(role='expert').count(),
            "admins":        CustomUser.objects.filter(role='admin').count(),
        }

    @staticmethod
    def get_feedback_stats():
        return {
            "total_feedback":    FeedbackReport.objects.count(),
            "pending_feedback":  FeedbackReport.objects.filter(status='pending').count(),
            "reviewed_feedback": FeedbackReport.objects.filter(status='reviewed').count(),
            "rejected_feedback": FeedbackReport.objects.filter(status='rejected').count(),
        }

    @staticmethod
    def get_overall_stats():
        total      = ScanSession.objects.count()
        counterfeit = ScanSession.objects.filter(result='counterfeit').count()

        return {
            "total_scans_ever":        total,
            "total_counterfeit_ever":  counterfeit,
            "overall_counterfeit_rate": round((counterfeit / total * 100), 2) if total > 0 else 0,
            "total_users":             CustomUser.objects.count(),
            "pending_feedbacks":       FeedbackReport.objects.filter(status='pending').count(),
        }