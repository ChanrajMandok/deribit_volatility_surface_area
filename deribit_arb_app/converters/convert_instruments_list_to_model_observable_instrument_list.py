from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.model.model_observable_instrument_list import \
                                       ModelObservableInstrumentList
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex

    #####################################################################
    # Converts Instruments List object to ModelObservableInstrumentList #
    #####################################################################

class ConvertInstrumentsListToModelObservableInstrumentList:
    
    def __init__(self) -> None:
        pass
    
    def convert(self, instruments: list) -> ModelObservableInstrumentList:
        
        try:
            list_model_subscribable_instruments = []
            for value in instruments:
                if isinstance(value, ModelSubscribableVolatilityIndex):
                    model_subscribable_vol_index = value
                if isinstance(value, ModelSubscribableIndex):
                    model_subscribable_index = value
                if isinstance(value, ModelSubscribableInstrument):
                    list_model_subscribable_instruments.append(value)
                
            x = ModelObservableInstrumentList(name='vsa_instruments_list',
                                              instruments = list_model_subscribable_instruments,
                                              volatility_index = model_subscribable_vol_index,
                                              index = model_subscribable_index
                                              )
            
            return x 

        except Exception as e:
            raise Exception(f"{self.__class__.__name__}: {e}")