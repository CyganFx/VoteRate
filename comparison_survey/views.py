from django.shortcuts import render, get_object_or_404

from comparison_survey.models import ComparisonSurvey


# shows all already created comparison surveys on home page
def get_all_c_surveys(request):
    all_surveys = ComparisonSurvey.objects.order_by('rating')
    print(f"All surveys: {all_surveys}")
    return render(request, 'comparison_survey/home.page.html', {'all_surveys': all_surveys})


def get_c_survey_by_id(request, id):
    c_survey = get_object_or_404(ComparisonSurvey, pk=id)
    return render(request, 'comparison_survey/home.page.html', {c_survey.id: c_survey})


def home(request):
    return render(request, 'comparison_survey/home.page.html')
