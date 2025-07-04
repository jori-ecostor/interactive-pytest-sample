import logging

logger = logging.getLogger(__name__)

def test_ui(user_input):
    logger.info('Wait for first input')
    rsp = user_input.wait("do something", timeout=30)
    assert rsp
    logger.info(f'1st rsp: {rsp}')

    logger.info('Wait for second input')
    rsp = user_input.get("Measure 12V power supply voltage")
    logger.info(f'2nd rsp: {rsp}')
    assert rsp
    voltage = float(rsp)

    assert voltage > 11.5 and voltage < 12.5
