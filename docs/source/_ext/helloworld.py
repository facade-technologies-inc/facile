"""
This is a tutorial extension from the sphinx documentation at
https://www.sphinx-doc.org/en/master/development/tutorials/helloworld.html

To use this extension, just use the .. helloworld:: directive. It will be replaced with the
paragraph "Hello World!" in the final documentation.
"""

from docutils import nodes
from docutils.parsers.rst import Directive


class HelloWorld(Directive):

    def run(self):
        paragraph_node = nodes.paragraph(text='Hello World!')
        return [paragraph_node]


def setup(app):
    app.add_directive("helloworld", HelloWorld)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }