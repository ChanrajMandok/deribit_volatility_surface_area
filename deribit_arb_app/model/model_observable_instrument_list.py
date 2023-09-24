from django.db import models
from django.contrib.postgres.fields import ArrayField

from deribit_arb_app.model.model_observable import ModelObservable
from deribit_arb_app.model.model_subscribable_instrument import \
                                     ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                      ModelSubscribableVolatilityIndex
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex

    ##########################################################
    # Model for BSM implied Volatility (observable) Objects #
    ##########################################################

class ModelObservableInstrumentList(ModelObservable, models.Model):
    
    name             = models.CharField(null=False, max_length=100, primary_key=True)
    instruments      = ArrayField(models.Field(ModelSubscribableInstrument), null=True)
    index            = models.ForeignKey(ModelSubscribableIndex, on_delete=models.CASCADE, null=True)
    volatility_index = models.ForeignKey(ModelSubscribableVolatilityIndex, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = False 