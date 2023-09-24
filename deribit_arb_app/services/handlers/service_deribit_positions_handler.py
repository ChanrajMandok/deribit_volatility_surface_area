import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.converters.converter_json_to_positions import \
                                       ConverterJsonToModelPositions
from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions

    ######################################
    # Service handles Deribit Positions  #
    ######################################

@singleton
class ServiceDeribitPositionsHandler():

    def __init__(self):

        self.store_deribit_positions = StoreDeribitPositions()
        self.positions = None
        
    def set_positions(self, result) -> dict[str,dict[str, ModelPosition]]:

        self.positions = ConverterJsonToModelPositions(json.dumps(result)).convert()
        positions = self.store_deribit_positions.set_deribit_positions(self.positions)
        return positions

