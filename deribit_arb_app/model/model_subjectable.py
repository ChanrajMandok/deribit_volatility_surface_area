from django.db import models


class ModelSubjectable(models.Model):

    key = models.CharField(null=False, max_length=100)

    class Meta:
        managed = False 
        