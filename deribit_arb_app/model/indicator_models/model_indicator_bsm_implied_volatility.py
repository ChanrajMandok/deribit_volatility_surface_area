from django.db import models

from deribit_arb_app.enums.enum_option_type import EnumOptionType
from deribit_arb_app.model.model_observable import ModelObservable
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex

    ##########################################################
    # Model for BSM implied Volatility (Observable) Objects #
    ##########################################################

class ModelIndicatorBsmImpliedVolatility(ModelObservable, models.Model):
    
    name                = models.CharField(max_length=50, null=False)
    option_type         = models.CharField(max_length=50, choices=EnumOptionType.choices(), null=False)
    instrument          = models.ForeignKey(ModelSubscribableInstrument, on_delete=models.CASCADE, related_name='instrument_IV')
    index               = models.ForeignKey(ModelSubscribableIndex, on_delete=models.CASCADE, related_name='index_IV')
    volatility_index    = models.ForeignKey(ModelSubscribableVolatilityIndex, on_delete=models.CASCADE, related_name='dvol')
    implied_volatility  = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    strike              = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    time_to_maturity    = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    spot                = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    timestamp           = models.IntegerField(null=True)
    
    def __init__(self, *args, **kwargs):
        instrument_name = kwargs.get('name', None)
        if instrument_name is not None and 'BSM Implied Volatility-' not in instrument_name:
            key = f"BSM Implied Volatility-{instrument_name}"
        else:
            key = instrument_name
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 
        
    def generate_key_from_instrument(self, instrument: ModelSubscribableInstrument):
        key = f"BSM Implied Volatility-{instrument.name}"
        return key
    
    def generate_key_from_str(self, instrument: str):
        key = f"BSM Implied Volatility-{instrument}"
        return key
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name} "
    