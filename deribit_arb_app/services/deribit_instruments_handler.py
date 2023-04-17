from deribit_arb_app.model.model_instrument import ModelInstrument
import json
from typing import Dict

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.converters.json_to_instruments import JsonToInstruments


@Singleton
class DeribitInstrumentsHandler:

    def __init__(self):

        self.store_instruments = StoreInstruments()

    def set_instruments(self, result) -> Dict[str, ModelInstrument]:

        self.store_instruments\
            .set_deribit_instruments(JsonToInstruments(json.dumps(result)).convert())

        return self.store_instruments.get_deribit_instruments()

