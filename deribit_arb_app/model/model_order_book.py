from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable


class ModelOrderBook(ModelSubjectable , models.Model):

    instrument_name       = models.CharField(null=False, max_length=100)
    best_bid_price        = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_ask_price        = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_bid_amount       = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    best_ask_amount       = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument_name = self.instrument_name
        
    class Meta:
        managed = False 
        
