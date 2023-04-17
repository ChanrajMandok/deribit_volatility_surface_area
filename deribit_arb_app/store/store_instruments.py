from typing import Dict, List, Optional
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.model.model_instrument import ModelInstrument


@Singleton
class StoreInstruments:

    def __init__(self):
        self.__deribit_instruments = {}
        
    def set_deribit_instruments(self, instruments: List[ModelInstrument]):
        for instrument in instruments:
            if not instrument.instrument_name in self.__deribit_instruments:
                self.__deribit_instruments[instrument.instrument_name] = None
            self.__deribit_instruments[instrument.instrument_name] = instrument

    def get_deribit_instruments(self) -> Dict[str, ModelInstrument]:
        return self.__deribit_instruments

    def get_deribit_instrument(self, instrument_name: str) -> Optional[ModelInstrument]:
        return self.__deribit_instruments[instrument_name]


