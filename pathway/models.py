from django.db import models
from questions.models import Stage
from django.contrib.auth import get_user_model


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


class PathwayPoint(models.Model):
    point = models.TextField()
    displayStage = models.ForeignKey(
        DisplayStage,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.point


class UserPathwayPoint(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    pathwayPoint = models.ForeignKey(
        PathwayPoint,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        default=1
    )

    def __str__(self):
        return str(self.user) + ": " + str(self.pathwayPoint.displayStage.firm)