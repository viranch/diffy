diffy - Easy diffing in Python
==============================

This is a (partial) Python port of https://github.com/samg/diffy.

> It provides a convenient way to generate a diff from two strings ~~or files~~. Instead of reimplementing the LCS diff algorithm Diffy uses battle tested Unix diff to generate diffs, and focuses on providing a convenient interface, and getting out of your way.

This module only generates HTML diffs (side-by-side not supported), and takes only strings as input (filenames not supported).

The HTML diff theme is taken as-is (because I'm bad at CSS!) from https://diff2html.xyz/ ([Demo](https://diff2html.xyz/demo.html)).

Getting Started
---------------

Here's an example of using Diffy to diff two strings

```python
import diffy
string1 = '''
Hello how are you
I'm fine
That's great
'''
string2 = '''
Hello how are you?
I'm fine
That's swell
'''
print diffy.Diff(string1, string2).generate(title='Testing Diffy!', names=['mystr1', 'mystr2'])
```

Write the output of the above script to an HTML file and open it in a browser to see your diff. Here's a screenshot of the HTML produced by above script:

<img src="https://raw.githubusercontent.com/viranch/diffy/master/screens/html.png" width="545">

Highlighting words is less performant for large diffs, in which case you can turn it off with `simple=True` argument:

```python
print diffy.Diff(string1, string2).generate(title='Testing Diffy!', names=['mystr1', 'mystr2'], simple=True)
```

If you want to see some lines before and after each changed line, pass `show_unchanged=3` or whatever number of lines you want:


```python
print diffy.Diff(string1, string2).generate(title='Testing Diffy!', names=['mystr1', 'mystr2'], simple=True, show_unchanged=3)
```
