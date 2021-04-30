from django.urls import path
from . import views

from comparison_survey import views as comparison_survey_views

urlpatterns = [
    path('home/', comparison_survey_views.home, name='home'),
    path('create/', comparison_survey_views.create, name='create'),
    path('results/', comparison_survey_views.results, name='results'),
    path('vote/', comparison_survey_views.vote, name='vote'),
]