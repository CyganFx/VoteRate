from django.urls import path
from comparison_survey.views import *


urlpatterns = [
    path('', get_all_c_surveys),
    # path('survey/<int:id>/', views.get_c_survey_by_id, name='comparison-survey-by-id'),
]
