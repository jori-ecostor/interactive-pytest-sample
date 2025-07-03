import logging
import pytest
from werkzeug import Request
from werkzeug import Response
import time

logger = logging.getLogger(__name__)

g_response = False

inputpage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Input</title>
</head>
<body>
    <form action="/userinput" method="POST">
        <input type="text" name="usertext" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>"""

def web_output_handler(request: Request):
    return Response(inputpage, content_type="text/html")

def web_input_handler(request: Request):
    global g_response
    g_response = True

    resp = request.form['usertext']

    rsp = f'Your answer: {resp}'

    return Response(rsp)

def wait_for_input():
    # TODO: add timeout
    while not g_response:
        time.sleep(.1)

    return

@pytest.fixture
def user_input(httpserver):
    httpserver.expect_request("/input").respond_with_handler(web_output_handler)
    httpserver.expect_request("/userinput").respond_with_handler(web_input_handler)
    # TODO: return class with .wait and .get objects
