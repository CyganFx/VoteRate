from django.urls import path
from comparison_survey.views import *

'''
we are here voterate.com/comparison_survey

    "description of url - url - template" # (optional->comment whole blocks of urls)

retrieve 
    all surveys - / - home.page.html # available for any user 
    survey by id - /<int:id> - survey.page.html # available for any user
    survey(s) - search.page.html
                by top number - /search/<int:num>
                by topic - /search/<str:topic>
                by date - /search/<int:year>/<int:month> # ?(shows starting from that date) 

# comparison surveys can be modified only by the creator of surveys

# below urls available for registered users

retrieve creators survey(s) - /my-surveys - dashboard.page.html
                             (/my-surveys/<int:id>) - survey.page.html
create new survey - /my-surveys/edit - survey.edit.page.html
update survey - /my-surveys/edit/id - survey.edit.page.html
delete survey - /my-surveys/remove/id - survey.edit.page.html, survey.page.html (button with request link)
'''

urlpatterns = [
    # for any user
    path('', RetrieveAllComparisonSurvey, name='comparison_survey-home'),
    path('<int:id>', RetrieveComparisonSurveyById, name='comparison_survey-by-id'),
    # TODO - implement search view for comparison survey
    # path('search/<int:num>'),
    # path('search/<str:topic>'),
    # path('search/<int:year>/<int:month>'),  # experiment
    # for authorized users
    path('my-surveys', RetrieveCreatorComparisonSurveys),
    path('my-surveys/<int:id>', RetrieveComparisonSurveyOfCreatorById),
    path('my-surveys/edit', CreateComparisonSurvey),
    path('my-surveys/edit/<int:id>', UpdateComparisonSurvey),
    path('my-surveys/remove/<int:id>', DeleteComparisonSurvey),
    # TODO - RateObject model CRUD urls needed to be implemented
]
