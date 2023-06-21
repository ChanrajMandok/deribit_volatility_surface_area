from singleton_decorator import singleton

from deribit_arb_app.observables.observable_indicator import ObservableIndicator
from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.model.model_instrument import ModelInstrument

    #########################################################
    # Store Manages & Stores Deribit ModelOrderBook Objects #
    #########################################################

@singleton
class StoreObservableOrderBooks():

    def __init__(self):
        self.__observable_order_books = {}

    def update_observable(self, order_book: ModelOrderBook):
        if not order_book.instrument_name in self.__observable_order_books:
            self.__observable_order_books[order_book.instrument_name] = ObservableIndicator(order_book)
        self.__observable_order_books[order_book.instrument_name].set_instance(order_book)
        # print(f"{order_book.instrument_name} updated: Bid: {order_book.best_bid_price} [{order_book.best_bid_amount}] - Ask: {order_book.best_ask_price} [{order_book.best_ask_amount}]")
        
    def get_observable(self, instrument: ModelInstrument):
        if not instrument.instrument_name in self.__observable_order_books:
            self.__observable_order_books[instrument.instrument_name] = ObservableIndicator(ModelOrderBook(instrument_name=instrument.instrument_name))
        x = self.__observable_order_books[instrument.instrument_name]
        return x 
    
    def remove_observable(self, instrument: ModelInstrument):
        if instrument.instrument_name in self.__observable_order_books:
            del self.__observable_order_books[instrument.instrument_name]
            
    def remove_observable_by_key(self, instrument_name: str):
        if instrument_name in self.__observable_order_books:
            del self.__observable_order_books[instrument_name]       