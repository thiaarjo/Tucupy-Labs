from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path('create-test-users/', views.create_test_users, name='create_test_users'),
]

