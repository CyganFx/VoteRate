from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Poll(models.Model):
    host_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    imageURL = models.CharField(default='', max_length=500)
    description = models.TextField()
    rating = models.FloatField(default=0)
    rateCounter = models.IntegerField(default=0)
    passedCounter = models.IntegerField(default=0)
    reportCounter = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class PollQuestion(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


class PollAnswer(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_id = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    votedNum = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return self.content


class PollVote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    passedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user_id} {self.poll_id} {self.answer_id} {self.passedAt}'


class UserPollRatings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'User: {self.user_id} Poll_ID: {self.poll_id} Rating: {self.rating}'


class PollStats(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    womenNum = models.IntegerField(default=0)
    womenPercentage = models.FloatField(default=0.0)
    manNum = models.IntegerField(default=0)
    manPercentage = models.FloatField(default=0.0)
    higher_education_num = models.IntegerField(default=0)
    higher_education_percentage = models.FloatField(default=0.0)
    countryNumKZ = models.IntegerField(default=0)
    countryKZPercentage = models.FloatField(default=0.0)
    countryNumUSA = models.IntegerField(default=0)
    countryUSAPercentage = models.FloatField(default=0.0)
    averageAge = models.FloatField(default=0.0)
    rateCounter = models.IntegerField(default=0)
    passedCounter = models.IntegerField(default=0)

    def __str__(self):
        return f'Poll ID: {self.poll_id} Passed counter: {self.passedCounter}'


class PollReports(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.TextField(max_length=50)
    report_text = models.TextField(max_length=200)
    at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Poll ID: {self.poll_id}, report type: {self.report_type}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)

    def __str__(self):
        return self.user.username + self.content
