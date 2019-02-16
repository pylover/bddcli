import re


class Response:
    body = None

    def __init__(self, status, stdout=None, stderr=None):
        self.status = status
        self.stdout = stdout
        self.stderr = stderr

    def to_dict(self):
        return dict(
            status=self.status,
            stdout=self.stdout,
            stderr=self.stderr
        )

    def __eq__(self, other: 'Response'):
        return self.status == other.status \
                and self.stdout == other.stdout \
                and self.stdout == other.stdout


