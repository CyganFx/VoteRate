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
    content = models.TextField()

    def __str__(self):
        return self.content


class PollVote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_id = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    passedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_id
