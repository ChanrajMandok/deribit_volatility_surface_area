import json
from typing import Dict

from singleton_decorator import singleton
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.converters.converter_json_to_instruments import ConverterJsonToInstruments
    
    #######################################
    # Service handles Deribit instruments #
    #######################################

@singleton
class ServiceDeribitInstrumentsHandler:

    def __init__(self):

        self.store_instruments = StoreInstruments()

    def set_instruments(self, result) -> Dict[str, ModelInstrument]:

        self.store_instruments\
            .set_deribit_instruments(ConverterJsonToInstruments(json.dumps(result)).convert())

        return self.store_instruments.get_deribit_instruments()

