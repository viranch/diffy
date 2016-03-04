from tempfile import NamedTemporaryFile

class TmpFiles:
    def __init__(self, contents=[]):
        self.files = []
        for content in contents:
            f = NamedTemporaryFile()
            f.write(content)
            f.flush()
            self.files.append(f)

    def __enter__(self):
        return [f.name for f in self.files]

    def __exit__(self, type, value, traceback):
        return [f.close() for f in self.files]
