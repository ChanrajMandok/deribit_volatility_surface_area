from django.db import models

    #####################################
    # Model for account Summary Objects #
    #####################################

class ModelAccountSummary(models.Model):

    available_funds                   =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    balance                           =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    currency                          =  models.CharField(max_length=50)
    delta_total                       =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    equity                            =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    futures_pl                        =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    futures_session_rpl               =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    futures_session_upl               =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    options_pl                        =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    options_delta                     =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    options_gamma                     =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    options_theta                     =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    options_session_rpl               =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    margin_balance                    =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    projected_initial_margin          =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    total_pl                          =  models.DecimalField(max_digits=20, decimal_places=8, null=False)

    initial_margin                    =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    maintenance_margin                =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    projected_delta_total             =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
    projected_maintenance_margin      =  models.DecimalField(max_digits=20, decimal_places=8, null=False)
   
   
    class Meta:
        managed = False

    def __repr__(self):
        return f"<{self.currency} Account Summary>"

