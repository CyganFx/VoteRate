from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAll, name='poll-home'),
    path('<int:id>', views.getByID),
    path('create/', views.createPoll, name='poll-create'),
    path('vote/', views.votePoll, name='poll-vote'),
    path('rate/', views.ratePoll, name='poll-rate'),
    path('<int:id>/stats/', views.pollStats, name='poll-stats'),
    path('report/', views.pollReport, name='poll-report'),
    path('reportsPage/', views.PollReportsPage, name='poll-reportsPage'),
    path('<int:id>/reports/', views.PollSpecificPollReports, name='poll-reports-specificPage'),
    path('<int:id>/delete/', views.PollDelete, name='poll-delete'),
    path('<int:id>/comments/', views.PollComments, name='poll-comments'),
    path('comments/', views.PollCommentsPost, name='poll-comments-post')
]
