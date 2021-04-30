from django.forms import ModelForm
from .models import Survey

class CreateSurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['question', 'option_one', 'option_two', 'option_three']