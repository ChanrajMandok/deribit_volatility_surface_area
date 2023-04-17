from deribit_arb_app.services.deribit_messaging import DeribitMessaging

deribit_messaging = DeribitMessaging

    ####################################################
    # Decorator imports derebit messaging for services #
    ####################################################


def decorator_deribit_messaging(func):
    """
    Decorator for importing deribit_messaging to a function.
    """
    def wrapper(*args, **kwargs):
        return func(*args, 
                     deribit_messaging = deribit_messaging,
                     **kwargs)

    return wrapper