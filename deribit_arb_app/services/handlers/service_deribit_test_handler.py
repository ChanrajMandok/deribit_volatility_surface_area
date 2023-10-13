import json

from singleton_decorator import singleton

from deribit_arb_app.enums.enum_field_name import EnumFieldName
from deribit_arb_app.converters.converter_json_to_test_response import \
                                             ConverterJsonToTestResponse

    ##################################################
    # Service Checks Deribit response from websocket #
    ##################################################

@singleton
class ServiceDeribitTestHandler():
    """
    Singleton class to manage and handle test operations related to Deribit.
    """

    def __init__(self) -> None:
        self.version = None

    def check_response(self, test_response: dict) -> None:
        """
        Checks and processes the provided test response to extract the version information.
        """
        result = ConverterJsonToTestResponse(json.dumps(test_response)).convert()

        if EnumFieldName.RESULT.value not in result:
            return None

        json_result = self.json_obj[EnumFieldName.RESULT.value]

        if EnumFieldName.VERSION.value not in json_result:
            return None

        self.version = json_result[EnumFieldName.VERSION.value]
