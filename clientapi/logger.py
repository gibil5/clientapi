import logging

DEFAULT_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"


def setup_logger():
    logger_instance = logging.getLogger("clientapi")
    logger_instance.setLevel(logging.DEBUG)
    logging.basicConfig(format=DEFAULT_FORMAT)
    return logger_instance


clientapi_logger = setup_logger()
