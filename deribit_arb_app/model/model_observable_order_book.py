from django.db import models
from deribit_arb_app.model.model_observable import ModelObservable

    #############################################
    # Model for Orderbook (Observable) Objects #
    #############################################

class ModelObservableOrderBook(ModelObservable , models.Model):

    name                  = models.CharField(null=False, max_length=100)
    best_bid_price        = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_ask_price        = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_bid_amount       = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_ask_amount       = models.DecimalField(max_digits=20, decimal_places=8, null=True)

    def __init__(self, *args, **kwargs):
        key = f"Orderbook {kwargs.get('name')}"
        super().__init__(key=key, *args, **kwargs)
        
    class Meta:
        managed = False 
        
