from deribit_arb_app.services.deribit_authentication import DeribitAuthentication

    ##############################################
    # Decorator provides derebit Authentication  #
    ##############################################

def decorator_deribit_authenticated(func):
    async def wrapper(*args, **kwargs):
        async with DeribitAuthentication().get_authenticated_websocket() as websocket:
            result = await func(websocket, *args, **kwargs)
            return result
    return wrapper