
class Documenter:
    def __init__(self, formatter_factory, fieldinfo=None):
        self.formatter_factory = formatter_factory
        self.fieldinfo = fieldinfo

    def write_response(self, formatter, response):
        formatter.write_header(f'Exit status: {response.status}', 3)

        if response.stdout:
            formatter.write_header('Standard Output', 4)
            formatter.write_paragraph(f'```\n{response.stdout}\n```')

        if response.stderr:
            formatter.write_header('Standard Error', 4)
            formatter.write_paragraph(f'```\n{response.stderr}\n```')

    def write_call(self, basecall, call, formatter):

        formatter.write_header(str(call), 3)

        if call.description:
            formatter.write_paragraph(call.description)

        if call.response:
            self.write_response(formatter, call.response)

    def document(self, story, outfile):
        basecall = story.base_call
        formatter = self.formatter_factory(outfile)
        formatter.write_header(basecall.title.capitalize(), 2)
        self.write_call(None, basecall, formatter)

        for call in story.calls:
            formatter.write_paragraph('---')
            formatter.write_header(f'WHEN: {call.title}', 2)
            self.write_call(basecall, call, formatter)

