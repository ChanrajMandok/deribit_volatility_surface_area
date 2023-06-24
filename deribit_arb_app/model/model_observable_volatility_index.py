from django.db import models
from deribit_arb_app.model.model_observable import ModelObservable

    #####################################################
    # Model for Volatility Index (subscribable) Objects #
    #####################################################

class ModelObservableVolatilityIndex(ModelObservable, models.Model):
    name         = models.CharField(max_length=255)
    timestamp    = models.IntegerField(null=False)
    volatility   = models.DecimalField(max_digits=20, decimal_places=8, null=False)

    def __init__(self, *args, **kwargs):
        key = f"deribit_volatility_index {kwargs.get('name')}"
        super().__init__(key=key, *args, **kwargs)
        
    class Meta:
        managed = False 
        
