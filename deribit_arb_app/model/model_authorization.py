from django.db import models


class ModelAuthorization(models.Model):

    access_token         = models.CharField(max_length=50, null=False)
    expires_in           = models.CharField(max_length=50, null=False)
    refresh_token        = models.CharField(max_length=50, null=False)
    scope                = models.CharField(max_length=50, null=False)
    token_type           = models.CharField(max_length=50, null=False)

    class Meta:
        managed = False 
        