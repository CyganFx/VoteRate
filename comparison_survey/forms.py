from django.forms import forms

from comparison_survey.models import ComparisonSurvey


class ComparisonSurveyForm(forms.ModelForm):
    class Meta:
        model = ComparisonSurvey
        fields = ('id', 'top_number', 'topic', 'user_id', 'description', 'rating', 'date_created')
