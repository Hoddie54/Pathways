from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from pathway.models import Industry, Firm, DisplayStage


class UserIndustry(models.Model):
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user) + ": " + str(self.industry)


class UserFirm(models.Model):
    firm = models.ForeignKey(
        Firm,
        on_delete=models.CASCADE
    )

    stage = models.ForeignKey(
        DisplayStage,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    order = models.IntegerField(blank=False, default=1000)

    def __str__(self):
        return str(self.user) + ": " + str(self.firm)