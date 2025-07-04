import logging
import webbrowser
import pytest
from werkzeug import Request
from werkzeug import Response
import time
import uuid

logger = logging.getLogger(__name__)

def make_prompt(prompt: str, response_id: str, response_required: bool):
    if response_required:
        html_input = f"""<input type="text" name="useraction" required>"""
    else:
        html_input = ""

    inputpage = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Input</title>
    </head>
    <body>
        <form action="/userinput" method="POST">
            <label for="useraction">Please do this: {prompt}</label>
            {html_input}
            <input type="hidden"
                id="response_id" name="response_id" value="{response_id}"/>
            <button type="submit">I did it</button>
        </form>
    </body>
    </html>"""

    return Response(inputpage, content_type="text/html")

def get_param(request: Request, name):
    if not name in request.form:
        return None
    else:
        return request.form[name]

class UserInputStorage:
    def __init__(self, httpserver):
        self.prompt = None
        self.response = None
        self.response_required = False
        self.prompt_id = str(uuid.uuid4())
        self.server = httpserver
        httpserver.expect_request("/input").respond_with_handler(self._web_output_handler)
        httpserver.expect_request("/userinput").respond_with_handler(self._web_input_handler)

    def _web_output_handler(self, request: Request):
        return make_prompt(self.prompt, self.prompt_id, self.response_required)

    def _web_input_handler(self, request: Request):
        prompt_id = get_param(request, 'response_id')

        if prompt_id == self.prompt_id:
            self.response = get_param(request, 'useraction')
            if not self.response:
                self.response = True

        rsp = f'Prompt: {self.prompt}\nYour answer: {self.response}\n(prompt id {prompt_id})'
        return Response(rsp)

    def get(self, prompt, timeout=60, response_required=True):
        """Prompt the user to input some data."""
        self.prompt = prompt
        self.response = None
        self.response_required = response_required
        self.timeout = timeout

        logger.info(f'Requesting user input: prompt {prompt}, response required: {response_required}')
        webbrowser.open(f'http://{self.server.host}:{self.server.port}/input')

        t_start = time.monotonic()
        while (not self.response
               and time.monotonic() - t_start < timeout):
            time.sleep(.1)

        return self.response

    def wait(self, prompt, timeout=60):
        "Wait for the user to complete an action."
        return self.get(prompt, timeout, response_required=False)

@pytest.fixture
def user_input(httpserver):
    i = UserInputStorage(httpserver)
    return i
