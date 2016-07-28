import subprocess
from tmpfiles import TmpFiles


class Differ:

    def __init__(self, string1, string2, show_unchanged=0):
        self.string1 = string1
        self.string2 = string2
        self.diff = None
        self.show_unchanged = show_unchanged

    def get_diff(self):
        if self.diff is None:
            with TmpFiles([self.string1, self.string2]) as tmp_files:
                self.diff = subprocess.Popen(['diff', '-U', str(self.show_unchanged)]+tmp_files, stdout=subprocess.PIPE).communicate()[0]
        return self.diff

    @staticmethod
    def is_line_diff_info(line):
        return (line.startswith('---') or line.startswith('+++') or line.startswith('\\') or line.startswith('@@'))

    def lines(self):
        return [line+"\n" for line in self.get_diff().split("\n") if not Differ.is_line_diff_info(line)]

    def chunks(self):
        old_state = None
        chunks = []
        for line in self.lines():
            state = line[0]
            if state == old_state:
                chunks[-1] += line
            else:
                chunks.append(line)
            old_state = state
        return chunks
