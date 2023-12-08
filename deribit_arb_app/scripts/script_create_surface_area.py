from deribit_arb_app.services.managers.service_implied_volatility_surface_area_task_manager import \
                                                      ServiceImpliedVolatilitySurfaceAreaTaskManager


def run():
    """
    This function runs the task for creating an implied volatility surface area producer.

    The task is specific to the cryptocurrency market, focusing on Bitcoin ('BTC'). 
    It initializes and runs a producer that generates an implied volatility surface 
    area, which is a graphical representation of the implied volatility of options 
    for different strikes and maturities.

    If `plot=True`, it also generates a plot of the implied volatility surface.

    :return: None
    """

    # Initialize the ServiceImpliedVolatilitySurfaceAreaTaskManager for Bitcoin
    manager = ServiceImpliedVolatilitySurfaceAreaTaskManager()

    # Create a producer for Bitcoin with plotting enabled
    manager.create_producer(currency='BTC', plot=False)
