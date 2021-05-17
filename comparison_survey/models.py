from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ComparisonSurvey(models.Model):
    """
    top_number is formed due to the number of rate-objects that belongs to survey
    views, rating fields used for statistical data
    """
    top_number = int
    topic = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    rating = models.FloatField(default=0.0)
    date_created = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.topic


class RateObject(models.Model):
    """model used to define objects of vote/rate action"""
    description = models.TextField()
    media = models.CharField(max_length=100)
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class ComparisonSurveyResult(models.Model):
    """keeps track of chosen rate records"""
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    rate_object = models.ForeignKey(RateObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Complaint(models.Model):
    """used by moderators"""
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id


class PassedSurvey(models.Model):
    """keeps track of user activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    last_passed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
