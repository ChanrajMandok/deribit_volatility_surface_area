import abc
import json
import traceback

from typing import TypeVar, Generic

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_authentication import \
                                                     ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector
                                  
# Generic type for the output model
M = TypeVar('M')
                                                      
    #############################################################
    # Interface for Retrieving infomation via Deribit Websocket #
    #############################################################
                                                      
class ServiceDeribitGetInterface(Generic[M],
                                 metaclass=abc.ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'get' method. """
        
        return (hasattr(subclass, 'get') and
                callable(subclass.get))
        
        
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def params(self):
        """Set the parameters for the Deribit API call."""
        raise NotImplementedError


    @abc.abstractmethod
    def method(self):
        """Set the method name for the Deribit API call."""
        raise NotImplementedError


    async def get(self) -> dict[str, dict[str, M]]:
        """
        Fetch the data for the specified currency and kind through a websocket connection.
        """
        try:
            message_id = ServiceDeribitMessaging().generate_id(method=self.method)
            
            msg = ModelMessage(method=self.method,
                               params=self.params,
                               msg_id=message_id)

            async with ServiceDeribitWebsocketConnector() as websocket:
                await ServiceDeribitAuthentication().authenticate(websocket)
                await websocket.send(json.dumps(msg.build_message()))

                while websocket.open:
                    response = await websocket.recv()
                    id, data = ServiceDeribitMessaging().message_handle(response)
                    if id == message_id:
                        return data
                    
        except Exception as e:
            self.logger_instance.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                       f"Stack trace: {traceback.format_exc()}")