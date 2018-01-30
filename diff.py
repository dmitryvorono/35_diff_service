import difflib
import html
from config import DIFF_CONFIG


def render_text_diff(initial_text, emended_text):
    out = []
    splited_initial_text = initial_text.splitlines(True)
    splited_emended_text = emended_text.splitlines(True)
    opcodes = get_opcodes(splited_initial_text, splited_emended_text)
    for opcode in opcodes:
        out.append(render_block(opcode,
                                splited_initial_text,
                                splited_emended_text))
    return ''.join(out)


def render_block(opcode, splited_initial_text, splited_emended_text):
    type_block = opcode[0]
    if type_block == 'replace':
        deleted_text = make_block_html_text('delete',
                                            splited_initial_text,
                                            opcode[1],
                                            opcode[2])
        inserted_text = make_block_html_text('insert',
                                             splited_emended_text,
                                             opcode[3],
                                             opcode[4])

        rendered_text = ''.join([deleted_text, inserted_text])
    elif type_block == 'delete' or type_block == 'delete_move':
        rendered_text = make_block_html_text(type_block,
                                             splited_initial_text,
                                             opcode[1],
                                             opcode[2])
    elif (type_block == 'move' or
          type_block == 'equal' or
          type_block == 'insert'):
        rendered_text = make_block_html_text(type_block,
                                             splited_emended_text,
                                             opcode[3],
                                             opcode[4])
    else:
        raise("Something's broken. I didn't expect a '" + type_block + "'.")
    return rendered_text


def make_block_html_text(type_block, splited_text, start, stop):
    html_escaped_text = html.escape(''.join(splited_text[start:stop]))
    return make_html_tag_for_diff_block(type_block, html_escaped_text)


def make_html_tag_for_diff_block(type_block, text):
    if type_block in DIFF_CONFIG:
        return '<{0} {1}>{2}</{0}>'.format(DIFF_CONFIG['tag'],
                                           DIFF_CONFIG[type_block],
                                           text)
    else:
        return '<{0}>{1}</{0}>'.format(DIFF_CONFIG['tag'], text)


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
                                              initial_text[opcode[1]:opcode[2]])
        if not equal_block:
            continue
        opcodes[opcodes.index(opcode)] = ('move',) + opcode[1:]
        opcodes[opcodes.index(equal_block)] = (('delete_move',) +
                                               equal_block[1:])


def find_equal_delete_block(inserted_text, opcodes, initial_text):
    for opcode in opcodes:
        if (opcode[0] == 'delete' and inserted_text == initial_text):
            return opcode


if __name__ == '__main__':
    import sys
    try:
        initial_text, emended_text = sys.argv[1:3]
    except ValueError:
        print("htmldiff: highlight the differences between two html files")
        print("usage: " + sys.argv[0] + " a b")
        sys.exit(1)
    print(render_text_diff(open(initial_text).read(),
                           open(emended_text).read()))
