from django.urls import path
from comparison_survey.views import *

urlpatterns = [
    # for any user
    path('', ComparisonSurveyAll.as_view(), name='comparison-survey-home'),
    path('<int:pk>', ComparisonSurveyDetail.as_view(), name='comparison-survey-by-id'),
    path('rate/<int:cs_pk>', RateCSurvey, name='comparison-survey-rate'),
    # TODO - implement search view for comparison survey
    # path('search/<int:num>'),
    # path('search/<str:topic>'),
    # path('search/<int:year>/<int:month>'),  # experiment
    # for authorized users
    path('my_surveys/all', RetrieveCreatorComparisonSurveys, name='my-surveys-all'),
    path('my_surveys/<int:pk>', RetrieveComparisonSurveyOfCreatorById, name='my-survey'),
    path('my_surveys/edit', CreateCSurvey.as_view(), name='my-surveys-new'),
    path('my_surveys/edit/<int:cs_pk>', EditCSurvey.as_view(), name='my-surveys-change'),
    path('my_surveys/remove/<int:id>', DeleteCSurvey, name='my-surveys-delete'),

    path('my_surveys/ro/<survey_id>', CreateRateObject, name='rate-object-new'),
    path('my_surveys/ro/remove/<int:ro_pk>', DeleteRateObject, name='rate-object-delete'),
]
