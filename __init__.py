from htmlformatter import HtmlFormatter
from differ import Differ


class Diff:

    def __init__(self, string1, string2, show_unchanged=0):
        self.differ = Differ(string1, string2, show_unchanged)

    def generate(self, title, names, simple=True, only_body=False):
        return HtmlFormatter(self.differ, title, names).generate(highlight_words=(not simple), only_body=only_body)
