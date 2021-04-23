from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Roles(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ComparisonSurvey(models.Model):
    top_number = int
    topic = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    # rate_objects = list(RateObject)
    rating = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.topic


class RateObject(models.Model):
    description = models.TextField()
    media = models.CharField(max_length=100)
    survey_id = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class ComparisonSurveyResult(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_id = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    rate_object_id = models.ForeignKey(RateObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Complaint(models.Model):
    survey_id = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id


class PassedSurvey(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_id = models.ForeignKey(ComparisonSurvey, on_delete=models.CASCADE)
    last_passed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
