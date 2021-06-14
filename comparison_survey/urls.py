from django.urls import path
from comparison_survey.views import *

from comparison_survey import views as comparison_survey_views

urlpatterns = [
    # for any user
    path('', ComparisonSurveyAll.as_view(), name='comparison-survey-home'),
    path('<int:pk>', ComparisonSurveyDetail.as_view(), name='comparison-survey-by-id'),

    path('category/<int:category_id>', CSurveysByCategory.as_view(), name='comparison-survey-by-category'),

    path('pass/<int:pk>', csurvey_pass_view, name='comparison-survey-pass'),
    path('pdf/<int:survey_id>', generate_pdf, name='comparison-survey-pdf'),

    # path('search/<str:topic>'),

    # for authorized users
    path('rate/<int:survey_id>', rate_csurvey, name='comparison-survey-rate'),
    path('my_surveys/all', retrieve_creator_comparison_surveys, name='my-surveys-all'),
    path('my_surveys/<int:pk>', retrieve_comparison_survey_of_creator_by_id, name='my-survey'),
    path('my_surveys/edit', CreateCSurvey.as_view(), name='my-surveys-new'),
    path('my_surveys/edit/<int:cs_pk>', EditCSurvey.as_view(), name='my-surveys-change'),
    path('my_surveys/remove/<int:id>', delete_csurvey, name='my-surveys-delete'),
    path('my_surveys/ro/<survey_id>', create_rate_object, name='rate-object-new'),
    path('my_surveys/ro/remove/<int:ro_pk>', delete_rate_object, name='rate-object-delete'),

    path('feedback/<int:survey_id>', feedback_actions, name='comparison-survey-feedback'),
    path('statistics/<int:survey_id>', statistics, name='comparison-survey-statistics'),
    path('complaint/<int:survey_id>', leave_complaint, name='comparison-survey-new-complaint'),
    path('complaint', ComplaintAll.as_view(), name='complaints-list'),
    path('complaints/for/<int:survey_id>', complaints_for_csurvey, name='comparison-survey-complaints')
]
