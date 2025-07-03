import logging

from conftest import wait_for_input

logger = logging.getLogger(__name__)

def test_ui(user_input):
    wait_for_input()
