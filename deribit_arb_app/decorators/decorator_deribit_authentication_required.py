from deribit_arb_app.services.deribit_api.service_deribit_authentication import \
                                                      ServiceDeribitAuthentication

    #############################################
    # Decorator Provides Deribit Authentication #
    #############################################

def decorator_deribit_authenticated(func):
    async def wrapper(*args, **kwargs):
        async with ServiceDeribitAuthentication().get_authenticated_websocket() as websocket:
            result = await func(websocket, *args, **kwargs)
            return result
    return wrapper