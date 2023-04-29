from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument


class ModelIndicatorAnnualisedReturnSpread(ModelSubjectable, models.Model):

    instrument_1     = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_1_IASR')
    instrument_2     = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_2_IASR')
    index           = models.ForeignKey(ModelIndex, on_delete=models.CASCADE)
    value           =  models.DecimalField(max_digits=20, decimal_places=8, null=True)
    amount          =  models.DecimalField(max_digits=20, decimal_places=8, null=True)


    def __init__(self, *args, **kwargs):
        key = f"Annualised_Spread-{kwargs['instrument_1'].instrument_name}-{kwargs['instrument_2'].instrument_name}"
        super().__init__(key=key, *args, **kwargs)

    class Meta:
        managed = False 