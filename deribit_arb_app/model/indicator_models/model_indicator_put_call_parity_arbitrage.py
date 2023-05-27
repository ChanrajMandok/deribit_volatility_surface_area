from django.db import models

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_subjectable import ModelSubjectable

    ######################################################
    # Model for Put-Call Arbitrage (subjectable) Objects #
    ######################################################

class ModelIndicatorPutCallParityArbitrage(ModelSubjectable, models.Model):

    put_instrument   = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='put_instrument_PCP')
    call_instrument  = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='call_instrument_PCP')
    index            = models.ForeignKey(ModelIndex, on_delete=models.CASCADE, related_name='index_PCP')
    value            = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    aribtrage        = models.BooleanField(null=False)

    #index needed to calculate BSM derived implied volatilty

    def __init__(self, *args, **kwargs):
        key = f"PutCall Pricing Assymetry- C:{kwargs['put_instrument'].instrument_name} C:{['put_instrument'].instrument_name}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 


    ### implement check to ensure that both instrumens have the same strike and ttm before 