from django.db import models
from django.conf import settings


class ScanSession(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    RESULT_CHOICES = [
        ('genuine', 'Genuine'),
        ('counterfeit', 'Counterfeit'),
        ('unknown', 'Unknown'),
    ]

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scans')
    image          = models.ImageField(upload_to='scans/%Y/%m/%d/')
    heatmap        = models.ImageField(upload_to='heatmaps/%Y/%m/%d/', null=True, blank=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result         = models.CharField(max_length=20, choices=RESULT_CHOICES, default='unknown')
    mse_score      = models.FloatField(null=True, blank=True)
    threshold      = models.FloatField(default=0.00540)
    confidence     = models.FloatField(null=True, blank=True)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Scan {self.id} — {self.user} — {self.result}"

    @property
    def is_genuine(self):
        return self.result == 'genuine'