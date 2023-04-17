from abc import ABC, abstractmethod
import asyncio
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.enums.direction import Direction
from deribit_arb_app.enums.order_type import OrderType
from deribit_arb_app.enums.exchange import Exchange


class ApiInterface(ABC):

    @abstractmethod
    def get_instruments(
        self,
        currency: str, 
        kind: str):
        pass
        
    @abstractmethod
    def send_order(
        self,
        instrument: ModelInstrument, 
        direction: Direction, 
        amount: float, 
        price: float):
        pass

    @abstractmethod
    def cancel_order(
        self, 
        exchange: Exchange,
        order_id: float):
        pass