from django.shortcuts import render
from .forms import CreateSurveyForm
from .models import Survey

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'date_posted': 'August 27'
    },
    {
        'author': 'asd2',
        'title': 'Blog Post 2',
        'date_posted': 'August 28'
    }
]


def home(request):
    context = {}
    return render(request, 'comparison_survey/home.html', context)

def create(request):
    form = CreateSurveyForm()
    context = {
        'form' : form
    }
    return render(request, 'comparison_survey/create.html', context)

def results(request):
    context = {}
    return render(request, 'comparison_survey/results.html', context)

def vote(request):
    context = {}
    return render(request, 'comparison_survey/vote.html', context)
