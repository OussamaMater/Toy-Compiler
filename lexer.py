#!/usr/bin/env python3
import sys
import re


class COLOR:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


"""Tags 
"""
KEYWORD = 'Keyword'
PAR = 'Parentheses'
OPR = 'Symbol'
INT = 'Integer'
ID = 'Variable'
JUNK = 'Junk'

"""A regex representation of each lexem
"""
token_expr = [
    (r'[\s]+', None),
    (r'let', KEYWORD),
    (r'set', KEYWORD),
    (r'in', KEYWORD),
    (r'print', KEYWORD),
    (r'[+*=\/-]', OPR),
    (r'[()]', PAR),
    (r'[0-9]+', INT),
    (r'([a-zA-Z]+)([0-9]*)([a-zA-Z]*)', ID),
    (r'.+', JUNK)
]


def lex(characters: str, token_exprs: list) -> list:
    """A function that returns a block of code as lexemes, let x = 1 + 1 -> [KEYWORD, ID, OPR, INT, OPR, INT]

    Args:
        characters (String): The code's block to be interpreted.
        token_exprs (List of tuples): A list that hold a model for each lexem and its tag.

    Returns:
        List: A list of tokens that represents the tag of each lexem.
    """
    pos = 0
    tokens = []
    while pos < len(characters):
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    if tag == 'Junk':
                        text = text.split(" ", 1)[0]
                        regex = re.compile(r'[\s]+')
                        match = regex.search(characters, pos)
                    token = (text, tag)
                    tokens.append(token)
                break
        pos = match.end(0)
    return tokens


filename = sys.argv[1]
if __name__ == '__main__':
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = lex(characters, token_expr)
    for token in tokens:
        if token[1] == 'Junk':
            print(f"[{COLOR.UNDERLINE}{token[0]}{COLOR.ENDC}, {COLOR.RED}{token[1]}{COLOR.ENDC}]. ")
        else:
            print(f"[{COLOR.BOLD}{token[0]}{COLOR.ENDC}, {COLOR.GREEN}{token[1]}{COLOR.ENDC}]. ")
