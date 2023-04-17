import json
from typing import Dict
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions
from deribit_arb_app.converters.json_to_positions import JsonToPositions
from deribit_arb_app.model.model_position import ModelPosition


@Singleton
class DeribitPositionsHandler:

    def __init__(self):

        self.store_deribit_positions = StoreDeribitPositions()
        self.positions = None
        
    def set_positions(self, result) -> Dict[str,Dict[str, ModelPosition]]:

        self.positions = JsonToPositions(json.dumps(result)).convert()
        positions = self.store_deribit_positions.set_deribit_positions(self.positions)
        return positions

