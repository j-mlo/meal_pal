from django.urls import path
from . import views

urlpatterns = [
    path('', views.weekly_planner_view, name="weekly_planner")
]