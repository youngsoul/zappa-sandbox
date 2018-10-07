import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



def sns_listener(event, context):
    logger.debug("SnsSubscriber.sns_listener")
    logger.debug(f"event: {event}")
    logger.debug(f"context: {context}")

    return "Done"
