from django.db import models
from django.contrib.auth import get_user_model

class Stage(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class QuestionPack(models.Model):
    name = models.CharField(max_length=150)
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        null=True
    )
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name + ": " + str(self.stage)


class Question(models.Model):
    title = models.CharField(max_length=150)
    question_pack = models.ForeignKey(
        QuestionPack,
        on_delete=models.SET_NULL,
        null=True,
        related_name='questionpack'
    )
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=100, choices=[('Easy', 'Easy'), ('Medium', 'Medium'),('Hard', 'Hard')], default='Medium')
    estimated_time = models.IntegerField(verbose_name='Estimated time in mins', default=5)

    def __str__(self):
        return self.title


class FirmQuestionPackConnector(models.Model):
    firm = models.ForeignKey(
        'pathway.Firm',
        on_delete=models.CASCADE
    )
    question_pack = models.ForeignKey(
        QuestionPack,
        on_delete=models.CASCADE,
        related_name='firmquestions'
    )

    def __str__(self):
        return str(self.firm) + ": " + str(self.question_pack)

class UserAnswer(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='useranswers'
    )
    my_answer = models.TextField(null=True)
    time_started = models.DateTimeField(null=True, blank=True)
    time_finished = models.DateTimeField(null=True, blank=True)
    attempt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ": " + str(self.question)