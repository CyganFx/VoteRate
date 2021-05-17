from django.urls import path
from comparison_survey.views import *

urlpatterns = [
    # for any user
    path('', RetrieveAllComparisonSurvey, name='comparison-survey-home'),
    path('<int:id>', RetrieveComparisonSurveyById, name='comparison-survey-by-id'),
    # TODO - implement search view for comparison survey
    # path('search/<int:num>'),
    # path('search/<str:topic>'),
    # path('search/<int:year>/<int:month>'),  # experiment
    # for authorized users
    path('my_surveys/all', RetrieveCreatorComparisonSurveys, name='my-surveys-all'),
    path('my_surveys/<int:id>', RetrieveComparisonSurveyOfCreatorById, name='my-survey'),
    path('my_surveys/edit', CreateComparisonSurvey, name='my-surveys-new'),
    path('my_surveys/edit/<int:id>', UpdateComparisonSurvey, name='my-surveys-change'),
    path('my_surveys/remove/<int:id>', DeleteComparisonSurvey, name='my-surveys-delete'),

    path('my_surveys/edit/ro', CreateRateObject, name='rate-object-new'),
    path('my_surveys/edit/ro/<int:id>', DeleteRateObject, name='rate-object-delete'),
    # TODO - RateObject model CRUD urls needed to be implemented
]
