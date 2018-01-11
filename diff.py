import difflib
import html


def textDiff(initial_text, emended_text):
    out = []
    initial_text = initial_text.splitlines(True)
    emended_text = emended_text.splitlines(True)
    try:
        seq_matcher = difflib.SequenceMatcher(None, initial_text,
                                    emended_text, autojunk=False)
    except TypeError:
        seq_matcher = difflib.SequenceMatcher(None, initial_text, emended_text)
    opcodes = seq_matcher.get_opcodes()
    find_moved_blocks(opcodes, initial_text, emended_text)
    for opcode in opcodes:
        if opcode[0] == "replace":
            out.append('<span class="red">' +
                       html.escape(''.join(initial_text[opcode[1]:opcode[2]])) +
                       '</span><span class="green">' +
                       html.escape(''.join(emended_text[opcode[3]:opcode[4]])) +
                       "</span>")
        elif opcode[0] == "delete" or opcode[0] == 'delete_move':
            out.append('<span class="red">' +
                       html.escape(''.join(initial_text[opcode[1]:opcode[2]])) +
                       "</span>")
        elif opcode[0] == "insert":
            out.append('<span class="green">' +
                       html.escape(''.join(emended_text[opcode[3]:opcode[4]])) +
                       "</span>")
        elif opcode[0] == "equal":
            out.append('<span>' +
                       html.escape(''.join(emended_text[opcode[3]:opcode[4]])) +
                       '</span>')
        elif opcode[0] == 'move':
            out.append('<span class="yellow">' +
                       html.escape(''.join(emended_text[opcode[3]:opcode[4]])) +
                       "</span>")
        else:
            raise("Um, something's broken. I didn't expect a '" + opcode[0] + "'.")
    return ''.join(out)


def find_moved_blocks(opcodes, initial_text, emended_text):
    for opcode in opcodes:
        if opcode[0] != 'insert':
            continue
        equal_block = find_equal_delete_block(emended_text[opcode[3]:opcode[4]],
                                              opcodes,
                                              initial_text)
        if not equal_block:
            continue
        opcodes[opcodes.index(opcode)] = ('move',) + opcode[1:]
        opcodes[opcodes.index(equal_block)] = (('delete_move',) +
                                               equal_block[1:])


def find_equal_delete_block(inserted_text, opcodes, initial_text):
    for opcode in opcodes:
        if opcode[0] == 'delete' and inserted_text == initial_text[opcode[1]:opcode[2]]:
            return opcode


if __name__ == '__main__':
    import sys
    try:
        initial_text, emended_text = sys.argv[1:3]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: " + sys.argv[0] + " a b")
        sys.exit(1)
    print(textDiff(open(initial_text).read(), open(emended_text).read()))
