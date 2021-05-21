from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAll, name='poll-home'),
    path('<int:id>', views.getByID),
    path('create/', views.createPoll, name='poll-create'),
    path('vote/', views.votePoll, name='poll-vote'),
    path('rate/', views.ratePoll, name='poll-rate'),
    path('<int:id>/stats', views.pollStats, name='poll-stats'),
    # path('<int:id>/comments', views.pollComments, name='poll-comments')
]
