from django.db import models
from questions.models import Stage


class Industry(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Firm(models.Model):
    name = models.CharField(max_length=150)
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
    )
    image = models.ImageField(upload_to='firms/')

    def __str__(self):
        return self.name

class DisplayStage(models.Model):
    name = models.CharField(max_length=150)
    firm = models.ForeignKey(
        Firm,
        on_delete=models.CASCADE
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name + ": " + str(self.firm)