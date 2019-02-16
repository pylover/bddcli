import sys

from easycli import SubCommand, Argument

from .formatters import *
from .documenter import Documenter


class DocumentarySubCommand(SubCommand):
    __command__ = 'document'
    __help__ = 'Generates CLI Documentation from standard input to standard ' \
        'output.'
    __arguments__ = [
        Argument(
            '-f',
            '--format',
            default='markdown',
            help='The output format. One of markdown, html. Default is '
                'markdown. currently only markdown is supported.'
        )
    ]

    formatters = {
        'markdown': MarkdownFormatter,
    }


    def convert_file(self, source, destination):
        from ..authoring import Story
        story = Story.load(source)
        story.document(
            destination,
            formatter_factory=self.formatters[self.args.format]
        )

    def __call__(self):
        self.convert_file(sys.stdin, sys.stdout)

