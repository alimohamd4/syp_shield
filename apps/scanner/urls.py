from django.urls import path
from .views import ScanCreateView, ScanHistoryView, ScanDetailView, AdminStatisticsView

urlpatterns = [
    path('scan/',            ScanCreateView.as_view(),      name='scan-create'),
    path('history/',         ScanHistoryView.as_view(),     name='scan-history'),
    path('history/<int:pk>/', ScanDetailView.as_view(),    name='scan-detail'),
    path('admin/stats/',     AdminStatisticsView.as_view(), name='admin-stats'),
]