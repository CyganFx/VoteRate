from django import forms
from comparison_survey.models import ComparisonSurvey, RateObject, Complaint


class ComparisonSurveyForm(forms.ModelForm):
    class Meta:
        model = ComparisonSurvey
        fields = ('topic', 'description', 'category',)


class RateObjectForm(forms.ModelForm):
    class Meta:
        model = RateObject
        fields = ('description', 'media',)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('reason',)
