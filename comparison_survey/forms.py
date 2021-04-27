from django import forms
from comparison_survey.models import ComparisonSurvey, RateObject


class ComparisonSurveyForm(forms.ModelForm):
    class Meta:
        model = ComparisonSurvey
        fields = '__all__'


class RateObjectForm(forms.ModelForm):
    class Meta:
        model = RateObject
        fields = '__all__'
