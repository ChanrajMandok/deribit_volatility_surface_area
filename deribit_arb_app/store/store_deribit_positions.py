from typing import  Optional
from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument

    ############################################
    # Store Manages & Stores Deribit Positions #
    ############################################

@singleton
class StoreDeribitPositions():
    
    # ['BTC-29DEC23':Position, 'BTC-30MAR22':Position ]

    def __init__(self):
        self.__positions = {}
        self.store_subscribable_instruments = Stores.store_subscribable_instruments


    def __len__(self) -> int:
        return len(self.__positions)


    def get_deribit_position(self, instrument: ModelSubscribableInstrument) -> Optional[ModelPosition]:
        if instrument.base_currency in self.__positions.keys():
            ccy_positions = self.positions[instrument.base_currency]
            return ccy_positions[instrument.name]
        else:
            return None


    def get(self, currency: str) -> dict[str,dict[str, ModelPosition]]:
        if not currency in self.__positions:
            self.__positions[currency] = {}
        return self.__positions[currency]


    def set(self, positions: list[ModelPosition]) -> dict[str,dict[str, ModelPosition]]:
        for position in positions:
            instrument = self.store_subscribable_instruments.get_via_key(position.instrument_name)
            if instrument:
                if not instrument.base_currency in self.__positions:
                    self.__positions[instrument.base_currency] = {}
                self.__positions[instrument.base_currency][instrument.name] = position
        return self.__positions
    
    
    def clear_store(self):
        self.__positions = {}