import cgi
from differ import Differ

class HtmlFormatter:

    def __init__(self, differ, title, names):
        self.differ = differ
        self.diff_title = title
        self.content_names = names

    def generate(self):
        return HtmlFormatter.wrap_lines(self.highlighted_words(), self.diff_title, self.content_names)

    def highlighted_words(self, wrap_lines=True):
        chunks = [chunk for chunk in self.differ.chunks() if chunk != '\ No newline at end of file\n']

        processed = []
        lines = []
        for index in range(len(chunks)):
            if index in processed:
                continue
            processed.append(index)
            chunk1 = chunks[index]
            if index+1 == len(chunks):
                lines.append(chunk1)
                continue
            chunk2 = chunks[index+1]

            if chunk1[0] == '-' and chunk2[0] == '+':
                line_diff = Differ(self.split_chars(chunk1), self.split_chars(chunk2), show_unchanged=True)
                hi1 = self.reconstruct_chars(line_diff, '-')
                hi2 = self.reconstruct_chars(line_diff, '+')
                processed.append(index+1)
                lines.extend(hi1+hi2)
            else:
                lines.append(chunk1)

        wrapped = []

        for line in lines:
            if line is not None:
                for l in line.split("\n"):
                    l = l.strip()
                    if wrap_lines:
                        l = HtmlFormatter.wrap_line(l)
                    wrapped.append(l)

        if wrap_lines:
            return [w for w in wrapped if w is not None]
        else:
            return [w[1:] for w in wrapped if w not in ['','+','-']]

    def split_chars(self, chunk):
        lines = []
        # .strip() is required to remove trailing "\n"
        for line in chunk.strip().split("\n"):
            line = line.strip()[1:] + "\\n"
            lines.extend(cgi.escape(char) for char in line)
        return "\n".join(lines) + "\n"

    def reconstruct_chars(self, line_diff, line_type):
        diff = ""
        enum = line_diff.chunks()
        for i in range(len(enum)):
            l = enum[i]
            if l.startswith(line_type) or "\n"+line_type in l:
                diff += self.highlight(l, line_type)
            elif l.startswith(' ') or "\n " in l:
                if i > 1 and i < len(enum) and len(l.split("\n")) < 4:
                    diff += self.highlight(l, line_type)
                else:
                    diff += ''.join([s[1:] for s in l.split("\n")]).replace("\n",'').replace('\\r', '\r').replace('\\n', '\n')
        # .strip() is required to remove trailing "\n"
        tag = 'ins' if line_type=='+' else 'del'
        return [line_type+l.replace('</{0}><{0}>'.format(tag),'').replace('<{0}></{0}>'.format(tag),'') for l in diff.strip().split("\n")]

    def highlight(self, lines, line_type):
        tag = 'ins' if line_type=='+' else 'del'
        lines = ''.join(l[1:] for l in lines.split("\n"))
        lines = lines.replace('\\n', '<LINE_BOUNDARY>').replace('\n','').replace('<LINE_BOUNDARY>','</{0}>\n<{0}>'.format(tag))
        return "<{1}>{0}</{1}>".format(lines, tag)

    @staticmethod
    def wrap_line(line):
        cleaned = HtmlFormatter.clean_line(line)
        # should fix this
        if cleaned == '':
            return None
        try:
            tag = {'+': 'ins', '-': 'del'}[line[0]]
        except:
            tag = 'dummy'
        return '    <tr><td class="d2h-{0} d2h-change"><div class="d2h-code-line d2h-{0} d2h-change"><span class="d2h-code-line-prefix">{1}</span><span class="d2h-code-line-ctn hljs">{2}</span></div></td></tr>'.format(tag, line[0], cleaned)

    @staticmethod
    def clean_line(line):
        return "\n".join(l[1:] for l in line.split("\n")).replace(' ', '&nbsp;')

    @staticmethod
    def wrap_lines(lines, title, names):
        prefix = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>'''+title+'''</title>

    <!--
        Diff to HTML (template.html)
        Author: rtfpessoa
    -->

    <style>
.d2h-code-line-prefix,
.line-num1 {
    float: left
}
.d2h-wrapper {
    text-align: left
}
.d2h-file-header {
    padding: 5px 10px;
    border-bottom: 1px solid #d8d8d8;
    background-color: #f7f7f7;
    font: 13px Helvetica, arial, freesans, clean, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol"
}
.d2h-file-stats {
    display: inline;
    font-size: 12px;
    text-align: center
}
.d2h-lines-added {
    text-align: right
}
.d2h-lines-added>* {
    background-color: #ceffce;
    border: 1px solid #b4e2b4;
    color: #399839;
    border-radius: 0 5px 5px 0;
    padding: 2px
}
.d2h-lines-deleted {
    text-align: left
}
.d2h-lines-deleted>* {
    background-color: #f7c8c8;
    border: 1px solid #e9aeae;
    color: #c33;
    border-radius: 5px 0 0 5px;
    padding: 2px
}
.d2h-file-name-wrapper {
    display: inline-flex
}
.d2h-file-name {
    line-height: 33px;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden
}
.d2h-file-diff,
.d2h-file-side-diff {
    overflow-x: scroll;
    overflow-y: hidden
}
.d2h-file-wrapper {
    border: 1px solid #ddd;
    border-radius: 3px;
    margin-bottom: 1em
}
.d2h-diff-table {
    border-collapse: collapse;
    font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 12px;
    width: 100%
}
.d2h-diff-tbody>tr>td>div {
    font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
    height: 16px;
    line-height: 16px
}
.d2h-files-diff {
    width: 100%
}
.d2h-file-side-diff {
    display: inline-block;
    width: 50%;
    margin-right: -4px
}
.d2h-code-line {
    display: block;
    white-space: nowrap;
    padding: 0 10px
}
.d2h-code-side-line {
    display: block;
    white-space: pre;
    padding: 0 10px;
    height: 18px;
    line-height: 18px;
    margin-left: 50px;
    color: inherit;
    overflow-x: inherit;
    background: 0 0
}
.d2h-code-line del,
.d2h-code-side-line del {
    display: inline-block;
    margin-top: -1px;
    text-decoration: none;
    background-color: #ffb6ba;
    border-radius: .2em
}
.d2h-code-line ins,
.d2h-code-side-line ins {
    display: inline-block;
    margin-top: -1px;
    text-decoration: none;
    background-color: #97f295;
    border-radius: .2em
}
.d2h-code-line-ctn,
.d2h-code-line-prefix {
    background: 0 0;
    padding: 0
}
.d2h-code-linenumber,
.d2h-code-side-linenumber {
    position: absolute;
    height: 18px;
    line-height: 18px;
    background-color: #fff;
    text-align: right;
    color: rgba(0, 0, 0, .3);
    cursor: pointer
}
.line-num1,
.line-num2 {
    width: 40px;
    padding-left: 3px;
    box-sizing: border-box;
    overflow: hidden;
    text-overflow: ellipsis
}
.line-num2 {
    float: right
}
.d2h-code-linenumber {
    box-sizing: border-box;
    width: 86px;
    padding-left: 2px;
    padding-right: 2px;
    border: solid #eee;
    border-width: 0 1px
}
.d2h-code-side-linenumber {
    box-sizing: border-box;
    width: 56px;
    padding-left: 5px;
    padding-right: 5px;
    border: solid #eee;
    border-width: 0 1px;
    overflow: hidden;
    text-overflow: ellipsis
}
.d2h-del {
    background-color: #fee8e9;
    border-color: #e9aeae
}
.d2h-ins {
    background-color: #dfd;
    border-color: #b4e2b4
}
.d2h-info {
    background-color: #f8fafd;
    color: rgba(0, 0, 0, .3);
    border-color: #d5e4f2
}
.d2h-del.d2h-change,
.d2h-ins.d2h-change {
    background-color: #ffc
}
del.d2h-change,
ins.d2h-change {
    background-color: #fad771
}
.d2h-file-diff .d2h-del.d2h-change {
    background-color: #fae1af
}
.d2h-file-diff .d2h-ins.d2h-change {
    background-color: #ded
}
.d2h-file-list-wrapper {
    margin-bottom: 10px
}
.d2h-file-list-wrapper a {
    text-decoration: none;
    color: #3572b0
}
.d2h-file-list-wrapper a:visited {
    color: #3572b0
}
.d2h-file-list-header {
    text-align: left
}
.d2h-file-list-title {
    font-weight: 700
}
.d2h-file-list-line {
    text-align: left;
    font: 13px Helvetica, arial, freesans, clean, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol"
}
.d2h-file-list-line .d2h-file-name {
    line-height: 21px
}
.d2h-file-list {
    display: block
}
.d2h-file-switch {
    display: none;
    font-size: 10px;
    cursor: pointer
}
    </style>
</head>'''

        body = '''
<body style="text-align: center; font-family: 'Source Sans Pro',sans-serif;">
<div id="diff">
    
<div class="d2h-wrapper">
  <div id="d2h-860589" class="d2h-file-wrapper" data-lang="txt">
  <div class="d2h-file-header">
    <span class="d2h-file-stats">
      <span class="d2h-lines-deleted">
        <span>{0}</span>
      </span>
      <span class="d2h-lines-added">
        <span>{1}</span>
      </span>
    </span>
    <span class="d2h-file-name-wrapper">
        <span class="d2h-file-name">&nbsp;{2}</span>
    </span>
  </div>
  <div class="d2h-file-diff">
    <div class="d2h-code-wrapper">
      <table class="d2h-diff-table">
        <tbody class="d2h-diff-tbody">
'''.format(names[0], names[1], title)

        suffix = '''
        </tbody>
      </table>
    </div>
  </div>
</div>

</div>

</div>
</body>
</html>
'''

        return '{0}\n{1}\n{2}\n{3}'.format(prefix, body, "\n".join(lines), suffix)
