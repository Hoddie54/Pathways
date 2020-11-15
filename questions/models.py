from django.db import models

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
    )
    question = models.TextField()
    answer = models.TextField()

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
