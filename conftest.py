import logging
import pytest
from werkzeug import Request
from werkzeug import Response
import time

logger = logging.getLogger(__name__)

g_response = False

def web_ui_handler(request: Request):
    global g_response
    g_response = True

    return Response("Heyo")

def wait_for_input():
    # TODO: add timeout
    while not g_response:
        time.sleep(.1)

    return

@pytest.fixture
def user_input(httpserver):
    httpserver.expect_request("/input").respond_with_handler(web_ui_handler)
    # TODO: return class with .wait and .get objects
