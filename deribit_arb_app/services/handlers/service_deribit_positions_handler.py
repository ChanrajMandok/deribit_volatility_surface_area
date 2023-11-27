import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.converters.converter_json_to_positions import \
                                       ConverterJsonToModelPositions
from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions

    ######################################
    # Service handles Deribit Positions  #
    ######################################

from singleton_decorator import singleton

@singleton
class ServiceDeribitPositionsHandler():
    """
    Singleton class responsible for handling the state and operations
    related to Deribit positions.
    """

    def __init__(self) -> None:
        self.store_deribit_positions = StoreDeribitPositions()
        self.positions = None
       
        
    def set_positions(self, result: dict) -> dict[str, dict[str, ModelPosition]]:
        """
        Processes, converts, and sets the positions based on the given result.
        """
        self.positions = ConverterJsonToModelPositions(json.dumps(result)).convert()
        positions = self.store_deribit_positions.set_deribit_positions(self.positions)
        return positions