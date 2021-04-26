from django.http import Http404
from django.shortcuts import render

from .models import ComparisonSurvey


def Retrieve_ListView(request):
    dataset = ComparisonSurvey.objects.all()
    return render(request, 'comparison_survey/home.page.html', {'dataset': dataset})


def Retrieve_DetailView(request, id):
    try:
        survey = ComparisonSurvey.objects.get(id=id)
    except ComparisonSurvey.DoesNotExist:
        raise Http404('Data does not exist')

    return render(request, 'comparison_survey/survey.create.html', {'survey': survey})

