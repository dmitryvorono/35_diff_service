#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough span, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string
import html


def isTag(x): return x[0] == "<" and x[-1] == ">"

def textDiff(a, b):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = []
    #a, b = html2list(a), html2list(b)
    a, b = a.split('\n'), b.split('\n')
    try: # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
      
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(
            tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
    
    for e in s.get_opcodes():
        if e[0] == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            out.append('<span class="red">'+html.escape(''.join(a[e[1]:e[2]])) + '</span><span class="green">'+html.escape(''.join(b[e[3]:e[4]]))+"</span>")
        elif e[0] == "delete":
            out.append('<span class="red">'+ html.escape(''.join(a[e[1]:e[2]])) + "</span>")
        elif e[0] == "insert":
            out.append('<span class="green">'+html.escape(''.join(b[e[3]:e[4]])) + "</span>")
        elif e[0] == "equal":
            #if e[1] == e[3] and e[2] == e[4]:
            out.append('<span>' + html.escape(''.join(b[e[3]:e[4]])) + '</span>')
            #else:
            #    out.append('<span class="red">'+html.escape(''.join(a[e[1]:e[2]])) + '</span><span class="yellow">'+html.escape(''.join(b[e[3]:e[4]])) + "</span>")
        else: 
            print("Um, something's broken. I didn't expect a '" + e[0] + "'.")
            raise
    return ''.join(out)

def html2list(x, b=0):
    mode = 'char'
    cur = ''
    out = []
    for c in x:
        if mode == 'tag':
            if c == '>': 
                if b: cur += ']'
                else: cur += c
                out.append(cur); cur = ''; mode = 'char'
            else: cur += c
        elif mode == 'char':
            if c == '<': 
                out.append(cur)
                if b: cur = '['
                else: cur = c
                mode = 'tag'
            elif c in string.whitespace: out.append(cur+c); cur = ''
            else: cur += c
    out.append(cur)
    return list(filter(lambda x: x is not '', out))

if __name__ == '__main__':
    import sys
    try:
        a, b = sys.argv[1:3]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: " + sys.argv[0] + " a b")
        sys.exit(1)
    print(textDiff(open(a).read(), open(b).read()))
    
