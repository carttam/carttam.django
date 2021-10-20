from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Define
max_length = 50


# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    dateTime = models.DateTimeField()

    def __str__(self):
        return '{} : {} ...'.format(self.user, self.title[:max_length]) if len(
            self.title) > max_length else '{} : {}'.format(self.user, self.title)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    question = models.ForeignKey(Question, on_delete=CASCADE)
    dateTime = models.DateTimeField()

    def __str__(self):
        return '{} : {} ...'.format(self.user, self.answer[:max_length]) if len(
            self.answer) > max_length else '{} : {}'.format(self.user, self.answer)


class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.user
