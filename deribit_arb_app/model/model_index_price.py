from django.db import models
from deribit_arb_app.model.model_subjectable import ModelSubjectable

    ###############################################
    # Model for Index Price (subjectable) Objects #
    ###############################################

class ModelIndexPrice(ModelSubjectable, models.Model):

    index_name      = models.CharField(max_length=255, null=False)
    price           = models.FloatField(null=False)
    timestamp       = models.IntegerField(null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_name = self.index_name

    class Meta:
        managed = False
        ordering = ['-timestamp']
        

    