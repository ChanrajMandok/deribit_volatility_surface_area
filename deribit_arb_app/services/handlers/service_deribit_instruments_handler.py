import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.converters.converter_json_to_instruments import \
                                            ConverterJsonToInstruments
    
    #######################################
    # Service handles Deribit instruments #
    #######################################

@singleton
class ServiceDeribitInstrumentsHandler():

    def __init__(self):

        self.store_subscribable_instruments = Stores.store_subscribable_instruments

    def set_instruments(self, result) -> dict[str, ModelSubscribableInstrument]:

        self.instruments = ConverterJsonToInstruments(json.dumps(result)).convert()
        instruments = self.store_subscribable_instruments.set_subscribables(self.instruments)
        return instruments

