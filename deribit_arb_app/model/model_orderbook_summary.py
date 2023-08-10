from django.db import models

    #######################################
    # Model for OrderBook Summary objects #
    #######################################

class ModelOrderbookSummary(models.Model):
    
    volume_usd               = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    volume                   = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    underlying_price         = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    underlying_index         = models.CharField(max_length=255, null=False)
    quote_currency           = models.CharField(max_length=255, null=False)
    price_change             = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    open_interest            = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    mid_price                = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    mark_price               = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    low                      = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    last                     = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    interest_rate            = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    instrument_name          = models.CharField(max_length=255, null=False, primary_key=True)
    high                     = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    estimated_delivery_price = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    creation_timestamp       = models.IntegerField(null=False)
    bid_price                = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    base_currency            = models.CharField(max_length=255, null=False)
    ask_price                = models.DecimalField(max_digits=20, decimal_places=8, null=True)


    class Meta:
        managed = False 