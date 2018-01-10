#!/usr/bin/python
"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough span, badly documented. Send me comments and patches."""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib, string
import html


def textDiff(a, b):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = []
    a, b = a.split('\n'), b.split('\n')
    try: # autojunk can cause malformed HTML, but also speeds up processing.
        s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    except TypeError:
        s = difflib.SequenceMatcher(None, a, b)
     
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(
            tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
    opcodes = s.get_opcodes()
    find_moved_blocks(opcodes, a, b)
    for e in opcodes:
        if e[0] == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            out.append('<span class="red">'+html.escape(''.join(a[e[1]:e[2]])) + '</span><span class="green">'+html.escape(''.join(b[e[3]:e[4]]))+"</span>")
        elif e[0] == "delete" or e[0] == 'delete_move':
            out.append('<span class="red">'+ html.escape(''.join(a[e[1]:e[2]])) + "</span>")
        elif e[0] == "insert":
            out.append('<span class="green">'+html.escape(''.join(b[e[3]:e[4]])) + "</span>")
        elif e[0] == "equal":
            out.append('<span>' + html.escape(''.join(b[e[3]:e[4]])) + '</span>')
        elif e[0] == 'move':
            out.append('<span class="yellow">'+html.escape(''.join(b[e[3]:e[4]])) + "</span>")
        else: 
            raise("Um, something's broken. I didn't expect a '" + e[0] + "'.")
    return ''.join(out)


def find_moved_blocks(opcodes, a, b):
    for opcode in opcodes:
        if opcode[0] != 'insert':
            continue
        equal_block = find_equal_deleted_block(b[opcode[3]:opcode[4]], opcodes, a)
        if not equal_block:
            continue
        opcodes[opcodes.index(opcode)] = ('move', opcode[1], opcode[2], opcode[3], opcode[4])
        opcodes[opcodes.index(equal_block)] = ('delete_move', equal_block[1], equal_block[2], equal_block[3], equal_block[4])


def find_equal_deleted_block(inserted_text, opcodes, a):
    for opcode in opcodes:
        if opcode[0] == 'delete' and inserted_text == a[opcode[1]:opcode[2]]:
            return opcode


if __name__ == '__main__':
    import sys
    try:
        a, b = sys.argv[1:3]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: " + sys.argv[0] + " a b")
        sys.exit(1)
    print(textDiff(open(a).read(), open(b).read()))
    
