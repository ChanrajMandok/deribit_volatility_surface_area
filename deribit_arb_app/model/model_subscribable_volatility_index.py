from django.db import models
from deribit_arb_app.model.model_subscribable import ModelSubscribable

    #####################################################
    # Model for Volatility Index (subscribable) Objects #
    #####################################################

class ModelSubscribableVolatilityIndex(ModelSubscribable, models.Model):
    name   = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = "deribit_volatility_index." +  f"{kwargs.get('name')}"

    class Meta:
        managed = False
        ordering = ['name']