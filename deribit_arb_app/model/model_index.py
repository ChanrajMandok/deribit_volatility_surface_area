from django.db import models
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable


class ModelIndex(ModelExchangeSubscribable, models.Model):

    index_name       = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = "deribit_price_index." + self.index_name

    class Meta:
        managed = False
        ordering = ['index_name']