import re


class Response:
    body = None

    def __init__(self, status, stdout=None, stderr=None):
        self.status = status
        self.stdout = stdout
        self.stderr = stderr

