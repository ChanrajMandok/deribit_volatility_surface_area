from django.db import models

    ############################
    # Model Observable Objects #
    ############################

class ModelObservable(models.Model):

    key = models.CharField(null=False, max_length=100)

    class Meta:
        managed = False 
        