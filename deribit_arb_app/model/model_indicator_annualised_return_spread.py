from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument


class ModelIndicatorAnnualisedReturnSpread(ModelSubjectable, models.Model):

    instrument1     = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_1_IASR')
    instrument2     = models.ForeignKey(ModelInstrument, on_delete=models.CASCADE, related_name='instrument_2_IASR')
    index           = models.ForeignKey(ModelIndex, on_delete=models.CASCADE)
    value           =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    amount          =  models.DecimalField(max_digits=20, decimal_places=8, null=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        key = f"ann-ret-spread-{self.instrument1.instrument_name}-{self.instrument2.instrument_name}"
        ModelSubjectable.__init__(key)

    class Meta:
        managed = False 