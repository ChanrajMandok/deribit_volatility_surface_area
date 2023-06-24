from django.db import models
from deribit_arb_app.model.model_observable import ModelObservable

    ###############################################
    # Model for Index Price (Observable) Objects #
    ###############################################

class ModelObservableIndexPrice(ModelObservable, models.Model):

    name            = models.CharField(max_length=255, null=False)
    price           = models.FloatField(null=False)
    timestamp       = models.IntegerField(null=False)

    def __init__(self, *args, **kwargs):
        key = f"index_price {kwargs.get('name')}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False
        ordering = ['-timestamp']
        

    