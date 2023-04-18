from typing import Dict, List, Optional

from singleton_decorator import singleton

from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_instrument import ModelInstrument

from deribit_arb_app.store.store_instruments import StoreInstruments


@singleton
class StoreDeribitPositions:
    
    # ['BTC-29DEC23':Position, 'BTC-30MAR22':Position ]

    def __init__(self):
        self.__positions = {}
        self.store_instruments = StoreInstruments()

    def get_deribit_position(self, instrument: ModelInstrument) -> Optional[ModelPosition]:
        if instrument.base_currency in self.__positions.keys():
            ccy_positions = self.positions[instrument.base_currency]
            return ccy_positions[instrument.instrument_name]
        else:
            return None

    def get_deribit_positions(self, currency: str) -> Dict[str,Dict[str, ModelPosition]]:
        if not currency in self.__positions:
            self.__positions[currency] = {}
        return self.__positions[currency]

    def set_deribit_positions(self, positions: List[ModelPosition]) -> Dict[str,Dict[str, ModelPosition]]:
        for position in positions:
            instrument = self.store_instruments.get_deribit_instrument(position.instrument_name)
            if instrument:
                if not instrument.base_currency in self.__positions:
                    self.__positions[instrument.base_currency] = {}
                self.__positions[instrument.base_currency][instrument.instrument_name] = position
        return self.__positions


