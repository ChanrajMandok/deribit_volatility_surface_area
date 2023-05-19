from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument

    ##########################################################
    # Model for BSM implied Volatility (subjectable) Objects #
    ##########################################################

class ModelIndicatorBsmImpliedVolatility(ModelSubjectable, models.Model):

    instrument     = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_IV')
    index          = models.ForeignKey(ModelIndex, on_delete=models.CASCADE, related_name='index_IV')
    value          = models.DecimalField(max_digits=20, decimal_places=8, null=True)

    def __init__(self, *args, **kwargs):
        key = f"BSM Implied Volatilty-{kwargs['instrument'].instrument_name}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 
        
    def generate_key(self, instrument):
        key = f"BSM Implied Volatility-{instrument.instrument_name}"
        return key
    
    