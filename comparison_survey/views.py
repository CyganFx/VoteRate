from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ComparisonSurveyForm
from .models import ComparisonSurvey

# TODO - implement search view for comparison survey
# TODO - implement CRUD for rateObject model (comparison objects)

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
delete survey - /my-surveys/edit/id - survey.edit.page.html, survey.page.html (button with request link)
'''


# #### Comparison Survey views (CRUD) ####

# FOR ANY USERS

# Returns all comparison surveys - home.page.html
def RetrieveAllComparisonSurvey(request, template='comparison_survey/home.page.html'):
    dataset = ComparisonSurvey.objects.all()
    return render(request, template, {'dataset': dataset})


# Returns exact comparison survey by id - survey.page.html
def RetrieveComparisonSurveyById(request, id, template='comparison_survey/survey.page.html'):
    try:
        survey = ComparisonSurvey.objects.get(id=id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, {'survey': survey})


# FOR AUTHORIZED USERS ONLY

# Returns all surveys created by exact user (user id retrieved from request.user) - dashboard.page.html
def RetrieveCreatorComparisonSurveys(request, template='comparison_survey/dashboard.page.html'):
    try:
        creatorSurveys = ComparisonSurvey.objects.get(user_id=request.user.id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, {'mySurveys': creatorSurveys})


# Returns exact comparison survey by id - survey.page.html
def RetrieveComparisonSurveyOfCreatorById(request, id, template='comparison_survey/survey.page.html'):
    try:
        survey = ComparisonSurvey.objects.get(id=id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, {'survey': survey})


# Used to create comparison survey and redirect user after creation to the user's surveys dashboard - survey.edit.page.html
def CreateComparisonSurvey(request, template='comparison_survey/survey.edit.page.html'):
    form = ComparisonSurveyForm(request.POST or None)
    if form.is_valid():
        form.date_created = timezone.now()
        form.user_id = request.user.id
        form.save()
        return redirect('/my-surveys')
    return render(request, template, {'form': form})


# Used to update comparison survey details - survey.edit.page.html
def UpdateComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    oldComparisonSurvey = get_object_or_404(ComparisonSurvey, pk=id)
    form = ComparisonSurveyForm(request.POST or None, instance=oldComparisonSurvey)
    if form.is_valid():
        form.save()
        return redirect(f'/my-surveys/{id}')
    return render(request, template, {'form': form})


# Used to delete comparison survey record - survey.edit.page.html, survey.page.html
def DeleteComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    try:
        data = get_object_or_404(ComparisonSurvey, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()
        return redirect('/my-surveys')
    return render(request, template)


# first place takes 4 score, second place 3 score ...
def ComparisonLogic():
    """
    if request.Method == GET (session not exist):
        create session for list of RateObjectIDs and for TOP
        insert all 16 RateObjects from db in session
        set session list ot some list variable
        extract 2 random objects from list variable
        delete everything from session
        insert new list variable with 14 objects to session
        return to user these 2 random objects

    else:
        chosen_obj_id = request.POST.get('chosed_obj_id')
        unchosen_obj_id = request.POST.get('unchosen_obj_id')

        insert chosen_obj_id and unchosen_obj_id to temp_db

        list_session = session.get('list_of_obj')

        top = get top from database

        if top == 1 and len(list_session) == 0: (in this case it's already 2 objects left and 1 pair)
            increase score by 10 for RateObject having id unchosen_obj_id (2nd place)
            increase score by 20 for RateObject having id chosen_obj_id (1st place)
            insert some data to ComparisonSurveyResult()
            return chosen_obj_id and redirect to congratulation page

        if len(list_session) == 0 and top != 1:
            list_session = select all chosen_RateObjectIDs from temp_db
            delete everything from temp_db except TOP and divide TOP by 2


        extract 2 random RateObjectIDs from list_session
        delete everything from session
        insert new list variable with len(list_session) objects to session

        return 2 objects to front
    """

    pass
