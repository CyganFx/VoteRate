from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ComparisonSurveyForm, RateObjectForm
from .models import ComparisonSurvey, RateObject


# #### Comparison Survey views (CRUD) ####

# FOR ANY USERS

def RetrieveAllComparisonSurvey(request, template='comparison_survey/home.page.html'):
    """Returns all comparison surveys - home.page.html"""
    dataset = ComparisonSurvey.objects.all()
    context = {
        'dataSet': dataset,
    }
    return render(request, template, context=context)


def RetrieveComparisonSurveyById(request, id, template='comparison_survey/survey.page.html'):
    """Returns exact comparison survey by id - survey.page.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=id)
        rateObjects = RateObject.objects.filter(survey_id=id)
        context = {
            'survey': survey,
            'rateObjects': rateObjects,
        }

    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, context=context)


# FOR AUTHORIZED USERS ONLY

def RetrieveCreatorComparisonSurveys(request, template='comparison_survey/dashboard.page.html'):
    """Returns all surveys created by exact user (user id retrieved from request.user) - dashboard.page.html"""
    try:
        creatorSurveys = ComparisonSurvey.objects.filter(user_id=request.user.id)
        context = {
            'mySurveys': creatorSurveys,
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('No surveys found for this creator')
    return render(request, template, context=context)


def RetrieveComparisonSurveyOfCreatorById(request, id, template='comparison_survey/survey.edit.page.html'):
    """Returns exact comparison survey by id - survey.page.html"""
    try:
        survey = ComparisonSurvey.objects.get(id=id)
        rateObjects = RateObject.objects.filter(survey_id=id)
        context = {
            'survey': survey,
            'rateObjects': rateObjects,
        }
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, template, context=context)


def CreateComparisonSurvey(request, template='comparison_survey/survey.new.page.html'):
    """Used to create comparison survey and redirect user after creation to the user's surveys dashboard - survey.edit.page.html"""
    form = ComparisonSurveyForm(request.POST or None)
    if form.is_valid():
        form.instance.user_id_id = request.user.id
        form.instance.date_created = timezone.now()
        form.save()
        return redirect('my-surveys-all')
    return render(request, template, {'form': form})


def UpdateComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to update comparison survey details - survey.edit.page.html"""
    oldComparisonSurvey = get_object_or_404(ComparisonSurvey, pk=id)
    form = ComparisonSurveyForm(request.POST or None, instance=oldComparisonSurvey)
    if form.is_valid():
        form.save()
        return redirect(f'my-surveys/{id}')
    return render(request, template, {'form': form})


def DeleteComparisonSurvey(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to delete comparison survey record - survey.edit.page.html, survey.page.html"""
    try:
        data = get_object_or_404(ComparisonSurvey, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()
        return redirect('my-surveys-all')
    return render(request, template)


# #### Rate Objects' views (CRUD) ####


def CreateRateObject(request, template='comparison_survey/rateobj.new.page.html'):
    """Used to create Rate Object and redirect user after creation to the comparison survey page that it belongs"""
    form = RateObjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('my-surveys-all')
    return render(request, template, {'form': form})


def DeleteRateObject(request, id, template='comparison_survey/survey.edit.page.html'):
    """Used to delete comparison survey record - survey.edit.page.html, survey.page.html"""
    try:
        data = get_object_or_404(RateObject, id=id)
    except Exception:
        raise Http404('Does Not Exist')

    if request.method == 'POST':
        data.delete()
        return redirect('my-surveys-all')
    return render(request, template)

# passSurvey

# retrieve statistics for comparison survey

# retrieve rateObjects rating
