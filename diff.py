import difflib
import html


def render_text_diff(initial_text, emended_text):
    out = []
    splited_initial_text = initial_text.splitlines(True)
    splited_emended_text = emended_text.splitlines(True)
    opcodes = get_opcodes(splited_initial_text, splited_emended_text)
    for opcode in opcodes:
        out.append(render_block(opcode, splited_initial_text, splited_emended_text))
    return ''.join(out)


def render_block(opcode, splited_initial_text, splited_emended_text):
    if opcode[0] == "replace":
        return ('<span class="red">' +
                html.escape(''.join(splited_initial_text[opcode[1]:opcode[2]])) +
                '</span><span class="green">' +
                html.escape(''.join(splited_emended_text[opcode[3]:opcode[4]])) +
                "</span>")
    elif opcode[0] == "delete" or opcode[0] == 'delete_move':
        return ('<span class="red">' +
                html.escape(''.join(splited_initial_text[opcode[1]:opcode[2]])) +
                "</span>")
    elif opcode[0] == "insert":
        return ('<span class="green">' +
                html.escape(''.join(splited_emended_text[opcode[3]:opcode[4]])) +
                "</span>")
    elif opcode[0] == "equal":
        return ('<span>' +
                html.escape(''.join(splited_emended_text[opcode[3]:opcode[4]])) +
                '</span>')
    elif opcode[0] == 'move':
        return ('<span class="yellow">' +
                html.escape(''.join(splited_emended_text[opcode[3]:opcode[4]])) +
                "</span>")
    else:
        raise("Um, something's broken. I didn't expect a '" + opcode[0] + "'.")


def get_opcodes(initial_text, emended_text):
    try:
        seq_matcher = difflib.SequenceMatcher(None, initial_text,
                                              emended_text, autojunk=False)
    except TypeError:
        seq_matcher = difflib.SequenceMatcher(None, initial_text, emended_text)
    opcodes = seq_matcher.get_opcodes()
    find_moved_blocks(opcodes, initial_text, emended_text)
    return opcodes


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
    print(render_text_diff(open(initial_text).read(), open(emended_text).read()))
