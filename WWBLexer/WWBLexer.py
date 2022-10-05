from pygments.lexer import RegexLexer
from pygments.token import Token

Token.Test



class WWBLexer(RegexLexer):
    name = 'WWB - Wireless Workbench Report file lexer'
    aliases = ['wwb']
    filenames = ['*.csv']

    tokens = {
        'root': [
            (r'".+"', Token.Title),
            (r'()')
        ],

    }