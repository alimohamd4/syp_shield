from django.urls import path
from .views import (
    MyPolicyView, AllPoliciesView, AppPolicyView,
    FeedbackCreateView, FeedbackListView, MyFeedbackView
)

urlpatterns = [
    path('my-policy/',       MyPolicyView.as_view(),       name='my-policy'),
    path('all/',             AllPoliciesView.as_view(),     name='all-policies'),
    path('app-policy/',      AppPolicyView.as_view(),       name='app-policy'),

    # Feedback — للخبراء
    path('feedback/',        FeedbackCreateView.as_view(),  name='feedback-create'),
    path('feedback/mine/',   MyFeedbackView.as_view(),      name='feedback-mine'),
    path('feedback/all/',    FeedbackListView.as_view(),    name='feedback-all'),
]