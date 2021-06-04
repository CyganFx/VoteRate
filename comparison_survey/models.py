from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """model defines one of the properties of Comparison Survey"""
    title = models.CharField(max_length=50, default='entertainment')

    def __str__(self):
        return self.title

class ComparisonSurvey(models.Model):
    """
    top_number is formed due to the number of rate-objects that belongs to survey
    views, rating fields used for statistical data
    """
    top_number = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, help_text='create catchy topics...')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, help_text='words are free... but not more than 500 symbols')
    rating = models.FloatField(default=0.0)
    date_created = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class RateObject(models.Model):
    """model used to define objects of vote/rate action"""
    description = models.TextField(max_length=50, help_text='rate object name here...')
    media = models.CharField(max_length=150, help_text='url of image here...')
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


"""
initial_list_of_ro -> send to user

list_of_chosen -> send to db
"""


class ComparisonSurveyResult(models.Model):
    """keeps track of chosen rate records"""
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    rate_object = models.ForeignKey(RateObject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Complaint(models.Model):
    """used by moderators"""
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(max_length=100, help_text='please indicate the reason for the complaint')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reason


class PassedSurvey(models.Model):
    """keeps track of user activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    last_passed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
