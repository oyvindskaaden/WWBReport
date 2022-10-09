#!/usr/bin/env python3
"""
    Module to read a WWB Report CSV
"""

from pprint import pprint
from WWBLexer.WWBLexer import WWBLexer
import json

import datetime


wwb_lexer = WWBLexer()

def main():
    with open("Testfiles/Test4.csv", "r") as file: 
        report_str: str = file.read().replace(", ", ";")
        #print(report_str)

        lexed_file = wwb_lexer.get_tokens_unprocessed(report_str)

        
        for i,j,k in lexed_file:
            print(i,j,k)
            continue
        
        tree = wwb_lexer.wwb_tree
        #print(tree)
        #pprint(tree)
        print(json.dumps(tree, indent=4))



if __name__ == '__main__':
    main()
    