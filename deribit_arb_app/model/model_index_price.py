from django.db import models
from deribit_arb_app.model.model_observable import ModelObservable

    ###############################################
    # Model for Index Price (Observable) Objects #
    ###############################################

class ModelIndexPrice(ModelObservable, models.Model):

    index_name      = models.CharField(max_length=255, null=False)
    price           = models.FloatField(null=False)
    timestamp       = models.IntegerField(null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_name = self.index_name

    class Meta:
        managed = False
        ordering = ['-timestamp']
        

    