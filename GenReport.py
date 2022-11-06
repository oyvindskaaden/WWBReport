#!/usr/bin/env python3
"""
    Module to read a WWB Report CSV
"""

import argparse
from pprint import pprint
from WWBLexer.WWBLexer import WWBLexer
from Templates.WWBMarkdown import to_markdown
import json
import pandas as pd

from datetime import datetime


wwb_lexer = WWBLexer()

parser = argparse.ArgumentParser(
                    prog = 'WWB Report generator',
                    description = 'Reads the CSV generated by WWB and outputs a file based on a template')

parser.add_argument('filename', type=str,
                    help='File to be scanned and generated')

parser.add_argument("-o", "--output",
                    help='Filename for the outputted file. If none is specified the output is routed to terminal.')

parser.add_argument("-f", "--format", choices=["md", "json", "json_minified"],
                    default="json",
                    help='Way of formatting the structure, default is json')


def main():
    args = parser.parse_args()

    with open(args.filename, "r") as file: 
        report_str: str = file.read()#.replace(", ", ";")
        #print(report_str)

        #lexed_file = wwb_lexer.get_tokens_unprocessed(report_str)

        
        tree = wwb_lexer.get_wwb_tree(report_str)#wwb_lexer.wwb_tree

        match args.format:
            case "md":
                print(to_markdown(tree))
            
            case "json":
                print(wwb_lexer)

            case "json_minified":
                print(wwb_lexer.to_json())



if __name__ == '__main__':
    main()



