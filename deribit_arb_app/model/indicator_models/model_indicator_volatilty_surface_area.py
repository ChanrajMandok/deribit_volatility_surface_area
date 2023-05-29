from django.db import models
from django.contrib.postgres.fields import ArrayField

from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    #########################################################
    # Model for Volatility Surface Area (subjectable) Array #
    #########################################################

class ModelIndicatorVolatilitySurfaceArea(ModelSubjectable, models.Model):

    volatilty_surface_area_array = ArrayField(models.Field(ModelIndicatorBsmImpliedVolatility), null= False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        managed = False 