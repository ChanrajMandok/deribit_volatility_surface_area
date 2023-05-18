from singleton_decorator import singleton
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices

    #########################################################
    # Service Handles Deribit Unsubscriptions via Websocket #
    #########################################################

@singleton
class ServiceDeribitUnsubscriptionHandler():

    def __init__(self):
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()

    def handle(self, result):

        if not "result" in result:
            return None

        params = result["result"]
        
        for unsub_channel in params:
            if not '.' in unsub_channel:
                return None

            if unsub_channel.split('.')[0] == "quote":
        
                self.store_subject_order_books.remove_subject_by_key(unsub_channel.split('.')[1])    
                
            elif unsub_channel.split('.')[0] ==  "deribit_price_index":    
            
                self.store_subject_index_prices.remove_subject_by_key(unsub_channel.split('.')[1])
