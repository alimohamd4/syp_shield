from django.db import models


class RolePolicy(models.Model):

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('user', 'User'),
        ('expert', 'Expert'),
    ]

    role              = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    daily_scan_limit  = models.IntegerField(default=2)
    can_view_heatmap  = models.BooleanField(default=False)
    can_view_mse      = models.BooleanField(default=False)
    can_export_report = models.BooleanField(default=False)
    can_give_feedback = models.BooleanField(default=False)
    history_days      = models.IntegerField(default=0)
    description       = models.TextField(blank=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Role Policy'
        verbose_name_plural = 'Role Policies'

    def __str__(self):
        return f"Policy — {self.role}"


class ScanLimit(models.Model):

    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='scan_limits',
        null=True,
        blank=True
    )
    device_id  = models.CharField(max_length=255, blank=True)
    date       = models.DateField(auto_now_add=True)
    scan_count = models.IntegerField(default=0)

    class Meta:
        unique_together = [['user', 'date'], ['device_id', 'date']]

    def __str__(self):
        identifier = self.user or self.device_id
        return f"{identifier} — {self.date} — {self.scan_count}"


class FeedbackReport(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    ]

    expert = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    scan = models.ForeignKey(
        'scanner.ScanSession',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    note       = models.TextField(blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.expert} on Scan #{self.scan.id}"


class AppPolicy(models.Model):

    SECTION_CHOICES = [
        ('data_collection', 'Data Collection'),
        ('image_processing', 'Image Processing'),
        ('security_storage', 'Security & Storage'),
        ('policy_updates', 'Policy Updates'),
    ]

    section   = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title     = models.CharField(max_length=200)
    content   = models.TextField()
    icon      = models.CharField(max_length=50, blank=True)
    order     = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title