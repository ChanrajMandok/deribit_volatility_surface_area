from django.db import models

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_observable import ModelObservable

    ##########################################################
    # Model for BSM implied Volatility (Observable) Objects #
    ##########################################################

class ModelIndicatorBsmImpliedVolatility(ModelObservable, models.Model):
    
    name                = models.CharField(max_length=50, null=False)
    instrument          = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_IV')
    index               = models.ForeignKey(ModelIndex, on_delete=models.CASCADE, related_name='index_IV')
    implied_volatilty   = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    strike              = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    time_to_maturity    = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    spot                = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    
    def __init__(self, *args, **kwargs):
        instrument_name = kwargs['name'] if 'name' in kwargs else None
        key = f"BSM Implied Volatilty-{instrument_name}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 
        
    def generate_key(self, instrument):
        key = f"BSM Implied Volatility-{instrument.name}"
        return key
    
    