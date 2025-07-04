import logging

logger = logging.getLogger(__name__)

def test_ui(user_input):
    logger.info('Wait for first input')
    user_input.get()
    logger.info('Wait for second input')
    user_input.get()
    assert None
