from django.db import models
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable


class ModelInstrument(ModelExchangeSubscribable, models.Model):

    instrument_name             = models.CharField(max_length=255)
    tick_size                   = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    taker_commission            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    settlement_period           = models.CharField(max_length=255, null=True)
    quote_currency              = models.CharField(max_length=255, null=True)
    option_type                 = models.CharField(max_length=255, null=True)
    min_trade_amount            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    maker_commission            = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    max_leverage                = models.IntegerField(null=True)
    kind                        = models.CharField(max_length=255, null=False)
    is_active                   = models.BooleanField(null=False)
    expiration_timestamp        = models.IntegerField(null=False)
    creation_timestamp          = models.IntegerField(null=False)
    contract_size               = models.IntegerField(null=False)
    base_currency               = models.CharField(max_length=255, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = "quote." + self.instrument_name

    class Meta:
        managed = False
        