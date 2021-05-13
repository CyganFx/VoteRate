from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ComparisonSurveyForm
from .models import ComparisonSurvey


# TODO - implement search view for comparison survey
# TODO - implement CRUD for rateObject model (comparison objects)

# #### Comparison Survey views (CRUD) ####

# FOR ANY USERS

def RetrieveAllComparisonSurvey(request, template='comparison_survey/home.page.html'):
    """Returns all comparison surveys - home.page.html"""
    dataset = ComparisonSurvey.objects.all()
    return render(request, template, {'dataset': dataset})


def RetrieveComparisonSurveyById(request, id, template='comparison_survey/survey.page.html'):
    """Returns exact comparison survey by id - survey.page.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, {'survey': survey})


# FOR AUTHORIZED USERS ONLY

def RetrieveCreatorComparisonSurveys(request, template='comparison_survey/dashboard.page.html'):
    """Returns all surveys created by exact user (user id retrieved from request.user) - dashboard.page.html"""
    try:
        creatorSurveys = ComparisonSurvey.objects.get(user_id=request.user.id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, {'mySurveys': creatorSurveys})


def RetrieveComparisonSurveyOfCreatorById(request, id, template='comparison_survey/survey.page.html'):
    """Returns exact comparison survey by id - survey.page.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, {'survey': survey})


def CreateComparisonSurvey(request, template='comparison_survey/survey.edit.page.html'):
    """Used to create comparison survey and redirect user after creation to the user's surveys dashboard - survey.edit.page.html"""
    form = ComparisonSurveyForm(request.POST or None)
    if form.is_valid():
        form.date_created = timezone.now()
        form.user_id = request.user.id
        form.save()
        return redirect('/my-surveys')
    return render(request, template, {'form': form})


def UpdateComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to update comparison survey details - survey.edit.page.html"""
    oldComparisonSurvey = get_object_or_404(ComparisonSurvey, pk=id)
    form = ComparisonSurveyForm(request.POST or None, instance=oldComparisonSurvey)
    if form.is_valid():
        form.save()
        return redirect(f'/my-surveys/{id}')
    return render(request, template, {'form': form})


def DeleteComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to delete comparison survey record - survey.edit.page.html, survey.page.html"""
    try:
        data = get_object_or_404(ComparisonSurvey, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()
        return redirect('/my-surveys')
    return render(request, template)

# #### Rate Objects' views (CRUD) ####
