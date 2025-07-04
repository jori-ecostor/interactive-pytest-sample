import logging
import pytest
from werkzeug import Request
from werkzeug import Response
import time
import uuid

logger = logging.getLogger(__name__)

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

class UserInputStorage:
    def __init__(self, httpserver):
        self.prompt = None
        self.response = None
        self.request_id = uuid.uuid4()
        httpserver.expect_request("/input").respond_with_handler(self._web_output_handler)
        httpserver.expect_request("/userinput").respond_with_handler(self._web_input_handler)

    def _web_output_handler(self, request: Request):
        # TODO: fill template with prompt
        return Response(inputpage, content_type="text/html")

    def _web_input_handler(self, request: Request):
        self.response = request.form['usertext']
        rsp = f'Your answer: {self.response}'
        return Response(rsp)

    def get(self, prompt=None, timeout=60):
        self.prompt = prompt
        self.response = None
        self.timeout = timeout

        t_start = time.monotonic()
        while (not self.response
               and time.monotonic() - t_start < timeout):
            time.sleep(.1)

@pytest.fixture
def user_input(httpserver):
    i = UserInputStorage(httpserver)
    return i
