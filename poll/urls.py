from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAll, name='poll-home'),
    path('<int:id>', views.getByID),
    path('create/', views.createPoll, name='poll-create'),
]
