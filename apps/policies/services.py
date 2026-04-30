from django.utils import timezone
from .models import TierPolicy, ScanLimit


class PolicyService:

    @staticmethod
    def get_policy(tier):
        try:
            return TierPolicy.objects.get(tier=tier)
        except TierPolicy.DoesNotExist:
            return None

    @staticmethod
    def can_scan(user):
        policy = PolicyService.get_policy(user.tier)

        if not policy:
            return False, "السياسة غير موجودة"

        if user.tier == 'obsidian':
            return True, "مسموح"

        today = timezone.now().date()
        scan_limit, _ = ScanLimit.objects.get_or_create(
            user=user,
            date=today
        )

        if scan_limit.scan_count >= policy.daily_scan_limit:
            return False, f"وصلت للحد اليومي ({policy.daily_scan_limit} scans)"

        return True, "مسموح"

    @staticmethod
    def increment_scan_count(user):
        if user.tier == 'obsidian':
            return

        today = timezone.now().date()
        scan_limit, _ = ScanLimit.objects.get_or_create(
            user=user,
            date=today
        )
        scan_limit.scan_count += 1
        scan_limit.save()

    @staticmethod
    def get_remaining_scans(user):
        if user.tier == 'obsidian':
            return 999

        policy = PolicyService.get_policy(user.tier)
        if not policy:
            return 0

        today = timezone.now().date()
        scan_limit, _ = ScanLimit.objects.get_or_create(
            user=user,
            date=today
        )
        return max(0, policy.daily_scan_limit - scan_limit.scan_count)