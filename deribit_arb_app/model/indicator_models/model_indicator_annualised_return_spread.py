from django.db import models

from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_observable import ModelObservable

    ############################################################
    # Model for Annualised Return Spread (Observable) Objects #
    ############################################################

class ModelIndicatorAnnualisedReturnSpread(ModelObservable, models.Model):
    
    name            =  models.CharField(max_length=50, null=False)
    instrument_1    =  models.ForeignKey(ModelSubscribableInstrument, on_delete=models.CASCADE, related_name='instrument_1_IASR')
    instrument_2    =  models.ForeignKey(ModelSubscribableInstrument, on_delete=models.CASCADE, related_name='instrument_2_IASR')
    index           =  models.ForeignKey(ModelSubscribableIndex, on_delete=models.CASCADE)
    value           =  models.DecimalField(max_digits=20, decimal_places=8, null=True)
    amount          =  models.DecimalField(max_digits=20, decimal_places=8, null=True)


    def __init__(self, *args, **kwargs):
        instrument_1 = kwargs['instrument_1'].name if 'instrument_1' in kwargs and kwargs['instrument_1'].name else None
        instrument_2 = kwargs['instrument_2'].name if 'instrument_2' in kwargs and kwargs['instrument_2'].name else None
        key = f"Annualised_Spread-{instrument_1}-{instrument_2}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 
        
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name} "
    