from django.utils import timezone
from .models import RolePolicy, ScanLimit


class PolicyService:

    @staticmethod
    def get_policy(role):
        try:
            return RolePolicy.objects.get(role=role)
        except RolePolicy.DoesNotExist:
            return None

    @staticmethod
    def can_scan(user=None, device_id=None):
        if user and user.is_authenticated and user.role_level >= 2:
            return True, "OK"
        role = user.role if (user and user.is_authenticated) else "guest"
        policy = PolicyService.get_policy(role)
        if not policy:
            return False, "NO_POLICY"
        today = timezone.now().date()
        if user and user.is_authenticated:
            limit, _ = ScanLimit.objects.get_or_create(user=user, date=today)
        else:
            if not device_id:
                return False, "NO_DEVICE"
            limit, _ = ScanLimit.objects.get_or_create(device_id=device_id, date=today)
        if limit.scan_count >= policy.daily_scan_limit:
            return False, "LIMIT_REACHED"
        return True, "OK"

    @staticmethod
    def increment_scan(user=None, device_id=None):
        today = timezone.now().date()
        if user and user.is_authenticated:
            if user.role_level >= 2:
                return
            limit, _ = ScanLimit.objects.get_or_create(user=user, date=today)
        else:
            limit, _ = ScanLimit.objects.get_or_create(device_id=device_id, date=today)
        limit.scan_count += 1
        limit.save()

    @staticmethod
    def get_remaining_scans(user=None, device_id=None):
        if user and user.is_authenticated and user.role_level >= 2:
            return 999
        role = user.role if (user and user.is_authenticated) else "guest"
        policy = PolicyService.get_policy(role)
        if not policy:
            return 0
        today = timezone.now().date()
        if user and user.is_authenticated:
            limit, _ = ScanLimit.objects.get_or_create(user=user, date=today)
        else:
            limit, _ = ScanLimit.objects.get_or_create(device_id=device_id, date=today)
        return max(0, policy.daily_scan_limit - limit.scan_count)