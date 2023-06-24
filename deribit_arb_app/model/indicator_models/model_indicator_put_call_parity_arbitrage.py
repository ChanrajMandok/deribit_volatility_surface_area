from django.db import models

from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_observable import ModelObservable

    ######################################################
    # Model for Put-Call Arbitrage (Observable) Objects #
    ######################################################

class ModelIndicatorPutCallVolArbitrage(ModelObservable, models.Model):

    put_instrument   = models.ForeignKey(ModelSubscribableInstrument, on_delete=models.CASCADE, related_name='put_instrument_PCP')
    call_instrument  = models.ForeignKey(ModelSubscribableInstrument, on_delete=models.CASCADE, related_name='call_instrument_PCP')
    index            = models.ForeignKey(ModelSubscribableIndex, on_delete=models.CASCADE, related_name='index_PCP')
    strike           = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    value            = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    aribtrage        = models.BooleanField(null=False)

    #index needed to calculate BSM derived implied volatility

    def __init__(self, *args, **kwargs):
        put_instrument = kwargs['put_instrument'].name if 'put_instrument' in kwargs and kwargs['put_instrument'].name else None
        call_instrument = kwargs['call_instrument'].name if 'call_instrument' in kwargs and kwargs['call_instrument'].name else None
        key = f"Put_Call Pricing Assymetry- C:{put_instrument} C:{call_instrument}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 