from abc import ABC, abstractmethod

from deribit_arb_app.enums.enum_exchange import EnumExchange
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind

    #########################################
    # Service Implements Interface for APIs #
    #########################################

class ServiceApiInterface(ABC):

    @abstractmethod
    def get_instruments(
        self,
        currency: EnumCurrency, 
        kind: EnumInstrumentKind):
        pass
        
    # @abstractmethod
    # def send_order(
    #     self,
    #     instrument: ModelInstrument, 
    #     direction: EnumDirection, 
    #     amount: float, 
    #     price: float):
    #     pass

    # @abstractmethod
    # def cancel_order(
    #     self, 
    #     exchange: EnumExchange,
    #     order_id: float):
    #     pass