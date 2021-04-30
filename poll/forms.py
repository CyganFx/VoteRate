from django.forms import TextInput, HiddenInput, ModelForm, Select, Textarea

from poll.models import *


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['host_id', 'category_id', 'title', 'imageURL', 'description']

    widgets = {
        "host_id": HiddenInput(),
        "category_id": Select(),
        "title": TextInput(attrs={
            'placeholder': 'Title'
        }),
        "imageURL": TextInput(attrs={
            'placeholder': 'Image URL'
        }),
        "description": Textarea(attrs={
            'placeholder': 'Description'
        })
    }
