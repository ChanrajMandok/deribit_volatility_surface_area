import abc
import json

from typing import Generic, TypeVar

# Generic type for the output model
M = TypeVar('M')

    #######################################################
    # Interface for handelling data via Deribit Websocket #
    #######################################################

class ServiceDeribitHanderInterface(Generic[M],
                                    metaclass=abc.ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'set' method. """
        
        return (hasattr(subclass, 'set') and
                callable(subclass.set))
            
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    abc.abstractmethod
    def converter_instance(self):
        """Converter to be used in convert raw json into specificed model format"""
        raise NotImplementedError
    
    abc.abstractmethod
    def store_instance(self):
        """Store instance which will be updated by hander"""
        raise NotImplementedError
    
    def set(self, 
            result: dict) -> dict[str, M]:
        """
        convert dict to specified model object and the updates relevent store
        """
        self.model_instances = self.converter_instance(json.dumps(result)).convert()
        self.store_instance.set(self.model_instances)
    