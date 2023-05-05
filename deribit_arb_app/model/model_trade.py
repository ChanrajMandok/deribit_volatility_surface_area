from django.db import models

    #########################
    # Model Trading Objects #
    #########################

class ModelTrade(models.Model):

    trade_seq           = models.IntegerField(null=False)
    trade_id            = models.CharField(max_length=255, null=False)
    timestamp           = models.IntegerField(null=False)
    tick_direction      = models.IntegerField(null=False)
    state               = models.CharField(max_length=255, null=False)
    self_trade          = models.BooleanField(null=False)
    reduce_only         = models.BooleanField(null=False)
    price               = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    post_only           = models.BooleanField(null=False)
    order_type          = models.CharField(max_length=255, null=False)
    order_id            = models.CharField(max_length=255, null=False)
    matching_id         = models.CharField(max_length=255, null=False)
    mark_price          = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    liquidity           = models.CharField(max_length=255, null=False)
    label               = models.CharField(max_length=255, null=False)
    instrument_name     = models.CharField(max_length=255, null=False)
    index_price         = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    fee_currency        = models.CharField(max_length=255, null=False)
    fee                 = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    direction           = models.CharField(max_length=255, null=False)
    amount              = models.DecimalField(max_digits=20, decimal_places=8, null=False)

    class Meta:
        managed = False 
        