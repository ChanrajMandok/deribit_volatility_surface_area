from django.db import models

    ##################################
    # Model for Subscribable Objects #
    ##################################

class ModelSubscribable(models.Model):

    channel_name = models.CharField(null=False, max_length=100)

    class meta:
        managed = False
        

    def __repr__(self):
        return f"{self.channel_name}" 
