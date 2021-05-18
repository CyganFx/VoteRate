from django import forms
from comparison_survey.models import ComparisonSurvey, RateObject


class ComparisonSurveyForm(forms.ModelForm):
    class Meta:
        model = ComparisonSurvey
        fields = ('topic', 'description',)


class RateObjectForm(forms.ModelForm):
    class Meta:
        model = RateObject
        fields = ('description', 'media',)
