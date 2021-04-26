from django.urls import path
from comparison_survey.views import *


'''
we are here voterate.com/comparison_survey

retrieve 
    all surveys - / # available for any user
    survey by id - /<int:id> # available for any user
    survey(s)
                by top number - /search/<int:_num>
                by topic - /search/<str:_topic>
                by date - /search/<int:year>/<int:month> # ?(shows starting from that date) 

# comparison surveys can be modified only by the creator of surveys 
create new survey - /edit # below urls available for registered users
update survey - /edit/id
delete survey - /edit/id
'''

urlpatterns = [
    path('', Retrieve_ListView, name='comparison_survey-home'),
    path('<int:id>', Retrieve_DetailView, name='comparison_survey-by-id'),
]

