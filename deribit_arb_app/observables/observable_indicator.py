from deribit_arb_app.observables.observable_interface import ObservableInterface

    ###############################################################################################
    # Observable wraps Indicators (Observable) in  subject-observer logic & adds to observer List #
    ###############################################################################################

class ObservableIndicator(ObservableInterface):
    
    def __init__(self, instance) -> None:
        super().__init__(instance)