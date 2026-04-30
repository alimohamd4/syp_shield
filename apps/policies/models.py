from django.db import models


class TierPolicy(models.Model):

    TIER_CHOICES = [
        ('standard', 'Standard'),
        ('gold', 'Gold'),
        ('obsidian', 'Obsidian'),
    ]

    tier                = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    daily_scan_limit    = models.IntegerField(default=5)
    history_days        = models.IntegerField(default=7)
    can_view_heatmap    = models.BooleanField(default=False)
    can_export_report   = models.BooleanField(default=False)
    can_view_mse        = models.BooleanField(default=False)
    description         = models.TextField(blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Tier Policy'
        verbose_name_plural = 'Tier Policies'

    def __str__(self):
        return f"Policy — {self.tier}"


class ScanLimit(models.Model):

    user       = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='scan_limits'
    )
    date       = models.DateField(auto_now_add=True)
    scan_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user} — {self.date} — {self.scan_count} scans"


class AppPolicy(models.Model):

    SECTION_CHOICES = [
        ('data_collection',  'Data Collection'),
        ('image_processing', 'Image Processing'),
        ('security_storage', 'Security & Storage'),
        ('policy_updates',   'Policy Updates'),
    ]

    section    = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    icon       = models.CharField(max_length=50, blank=True)
    order      = models.IntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title