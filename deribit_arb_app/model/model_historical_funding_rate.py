from django.db import models


class ModelHistoricalFundingRate(models.Model):

    timestamp           = models.IntegerField(null=False)
    index_price         = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    prev_index_price    = models.DecimalField(max_digits=20, decimal_places=8, null=False)   
    interest_8h         = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    interest_1h         = models.DecimalField(max_digits=20, decimal_places=8, null=False)

    class Meta:
        managed = False 
        

