from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='comparison_survey-home'),
]