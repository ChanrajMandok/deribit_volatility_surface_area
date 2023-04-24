from singleton_decorator import singleton

from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.subjects.subject_order_book import SubjectOrderBook

    #########################################################
    # Store Manages & Stores Deribit ModelOrderBook Objects #
    #########################################################

@singleton
class StoreSubjectOrderBooks:

    def __init__(self):
        self.__subject_order_books = {}

    def update_subject(self, order_book: ModelOrderBook):
        if not order_book.instrument_name in self.__subject_order_books:
            self.__subject_order_books[order_book.instrument_name] = SubjectOrderBook(order_book)
        self.__subject_order_books[order_book.instrument_name].set_instance(order_book)
        print(f"{order_book.instrument_name} updated: {order_book.best_bid_price}:{order_book.best_bid_amount} - {order_book.best_ask_price}:{order_book.best_ask_amount}")
        
    def get_subject(self, instrument: ModelInstrument) -> SubjectOrderBook:
        if not instrument.instrument_name in self.__subject_order_books:
            self.__subject_order_books[instrument.instrument_name] = SubjectOrderBook(ModelOrderBook(instrument_name=instrument.instrument_name))
        return self.__subject_order_books[instrument.instrument_name]