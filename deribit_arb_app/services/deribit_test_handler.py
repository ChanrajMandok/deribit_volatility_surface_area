import json
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.converters.json_to_test_response import JsonToTestResponse
from deribit_arb_app.enums.field_name import FieldName


@Singleton
class DeribitTestHandler:

    def __init__(self):

        self.version = None

    def check_response(self, test_response):

        result = JsonToTestResponse(json.dumps(test_response)).convert()

        if FieldName.RESULT.value not in result:
            return None

        json_result = self.json_obj[FieldName.RESULT.value]

        if FieldName.VERSION.value not in json_result:
            return None

        self.version = json_result[FieldName.VERSION.value]
