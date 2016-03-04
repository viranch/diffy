from htmlformatter import HtmlFormatter
from differ import Differ

class Diff:

    def __init__(self, string1, string2, show_unchanged=False):
        self.differ = Differ(string1, string2)

    def generate(self, title, names):
        return HtmlFormatter(self.differ, title, names).generate()
