from django.db import models

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_observable import ModelObservable

    ############################################################
    # Model for Annualised Return Spread (Observable) Objects #
    ############################################################

class ModelIndicatorAnnualisedReturnSpread(ModelObservable, models.Model):
    
    name            = models.CharField(max_length=50, null=False)
    instrument_1    =  models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_1_IASR')
    instrument_2    =  models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_2_IASR')
    index           =  models.ForeignKey(ModelIndex, on_delete=models.CASCADE)
    value           =  models.DecimalField(max_digits=20, decimal_places=8, null=True)
    amount          =  models.DecimalField(max_digits=20, decimal_places=8, null=True)


    def __init__(self, *args, **kwargs):
        instrument_1 = kwargs['instrument_1'].instrument_name if 'instrument_1' in kwargs and kwargs['instrument_1'].instrument_name else None
        instrument_2 = kwargs['instrument_2'].instrument_name if 'instrument_2' in kwargs and kwargs['instrument_2'].instrument_name else None
        key = f"Annualised_Spread-{instrument_1}-{instrument_2}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 