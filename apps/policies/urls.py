from django.urls import path
from .views import MyPolicyView, AllPoliciesView, AppPolicyView

urlpatterns = [
    path('my-policy/',  MyPolicyView.as_view(),  name='my-policy'),
    path('all/',        AllPoliciesView.as_view(), name='all-policies'),
    path('app-policy/', AppPolicyView.as_view(),  name='app-policy'),
]