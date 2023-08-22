import logging

# create logger            deribit_arb_app.backtesting'
logger = logging.getLogger('deribit_arb_app.store     ')
logger.setLevel(logging.DEBUG)

logger.propagate = 0

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
