from django.forms import TextInput, ModelForm, Select, Textarea
from django import forms
from poll.models import *


# class PollForm(ModelForm):
#     # host_id = forms.IntegerField(widget=forms.HiddenInput())
#     # host_id = forms.IntegerField()
#
#     class Meta:
#         model = Poll
#         fields = ['host_id', 'category_id', 'title', 'imageURL', 'description']
#
#     widgets = {
#         "host_id": Select(),
#         "category_id": Select(),
#         "title": TextInput(attrs={
#             'placeholder': 'Title'
#         }),
#         "imageURL": TextInput(attrs={
#             'placeholder': 'Image URL'
#         }),
#         "description": Textarea(attrs={
#             'placeholder': 'Description'
#         })
#     }
#
