from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable


class ModelPosition(ModelSubjectable, models.Model):

    instrument_name                  = models.CharField(max_length=50)
    kind                             = models.CharField(max_length=10, null=True)
    direction                        = models.CharField(max_length=10, null=True)
    size                             = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    size_currency                    = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    average_price                    = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    estimated_liquidation_price      = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    initial_margin                   = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    interest_value                   = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    maintenance_margin               = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    open_orders_margin               = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    leverage                         = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    delta                            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    gamma                            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    vega                             = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    theta                            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    index_price                      = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    mark_price                       = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    settlement_price                 = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    realized_profit_loss             = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    floating_profit_loss             = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    total_profit_loss                = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    realized_funding                 = models.DecimalField(max_digits=20, decimal_places=8, null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument_name = self.instrument_name

    class Meta:
        managed = False 
        



