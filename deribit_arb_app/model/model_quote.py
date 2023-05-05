from django.db import models

    ###########################
    # Model for quote Objects #
    ###########################

class ModelQuote(models.Model):

    price       = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    size        = models.DecimalField(max_digits=20, decimal_places=8, null=False)
 
    class Meta:
        managed = False 
        