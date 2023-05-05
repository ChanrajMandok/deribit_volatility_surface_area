from django.db import models
from deribit_arb_app.model.model_trade import ModelTrade

    ###########################
    # Model for order objects #
    ###########################

class ModelOrder(models.Model):

    web                     = models.BooleanField(null=False)
    time_in_force           = models.CharField(max_length=255, null=False)
    replaced                = models.BooleanField(null=False)
    reduce_only             = models.BooleanField(null=False)
    profit_loss             = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    price                   = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    post_only               = models.BooleanField(null=False)
    order_type              = models.CharField(max_length=255, null=False)
    order_state             = models.CharField(max_length=255, null=False)
    order_id                = models.CharField(max_length=255, null=False, primary_key=True)
    max_show                = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    last_update_timestamp   = models.IntegerField(null=False)
    label                   = models.CharField(max_length=255, null=False)
    is_liquidation          = models.BooleanField(null=False)
    instrument_name         = models.CharField(max_length=255, null=False)
    filled_amount           = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    direction               = models.CharField(max_length=255, null=False)
    creation_timestamp      = models.IntegerField(null=False)
    commission              = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    average_price           = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    api                     = models.BooleanField(null=False)
    amount                  = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    trades                  = models.ManyToManyField(ModelTrade)

    class Meta:
        managed = False 
        



