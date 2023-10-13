from deribit_arb_app.converters import logger
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
    """
    A class to convert a list of various instrument models to a unified
    ModelObservableInstrumentList. This class acts as a converter and wraps the
    provided instruments list into a ModelObservableInstrumentList instance.
    """
    
    def convert(self, instruments: list) -> ModelObservableInstrumentList:
        """
        Converts a list of instruments to a ModelObservableInstrumentList.
        
        The method iterates over each instrument in the provided list. It categorizes
        each instrument according to its type and assigns it to the appropriate attribute
        in the ModelObservableInstrumentList instance. If an instrument is of type
        ModelSubscribableVolatilityIndex or ModelSubscribableIndex, it will be individually
        assigned. All other instruments of type ModelSubscribableInstrument will be
        appended to a list and assigned collectively.
        """
        
        try:
            # Check the type of each instrument and categorize accordingly.
            list_model_subscribable_instruments = []
            for value in instruments:
                if isinstance(value, ModelSubscribableVolatilityIndex):
                    model_subscribable_vol_index = value
                if isinstance(value, ModelSubscribableIndex):
                    model_subscribable_index = value
                if isinstance(value, ModelSubscribableInstrument):
                    list_model_subscribable_instruments.append(value)
             
            model_observable_instrument_list = \
                ModelObservableInstrumentList(name='vsa_instruments_list',
                                              index = model_subscribable_index,
                                              volatility_index = model_subscribable_vol_index,
                                              instruments = list_model_subscribable_instruments,
                                              )
            
            return model_observable_instrument_list 

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")