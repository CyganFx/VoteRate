from django.urls import path
from comparison_survey.views import *


urlpatterns = [
    path('', home, name='comparison_survey-home'),
    # path('survey/<int:id>/', views.get_c_survey_by_id, name='comparison-survey-by-id'),
]

