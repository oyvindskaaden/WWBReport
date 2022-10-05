#!/usr/bin/env python3
"""
    Module to read a WWB Report CSV
"""

import re
from enum import Enum, auto

class Report(Enum):
    TAG                 = auto()
    SHOW_NAME           = auto()
    SHOW_INFO           = auto()
    HEADER              = auto()
    RF_ZONE             = auto()
    ACTIVE_CHANNELS     = auto()
    BACKUP_FREQUENCY    = auto()
    INCLUSION_GROUP     = auto()
    PARAMETERS          = auto()
    INCLUSIONS          = auto()
    INCLUSION_LIST      = auto()
    EXCLUSIONS          = auto()
    EXCLUSIONS_TV       = auto()
    EXCLUSIONS_OTHER    = auto()
    CREATED             = auto()
    GENERATED           = auto()


    


with open("Testfiles/Test2.csv", "r") as file: 

    report: list[str] = file.readlines()

    partIndex: list[int] = []
    parts: list[list[str]] = [[]]

    i: int = 0
    for n, l in enumerate(report):
        if l == "\n":
            partIndex.append(n)
            print(parts[i])
            parts.append([])
            i += 1
        else:
            parts[i].append(l.strip())
        print(n, l.strip())

    #print(partIndex)
    print(parts[i])


    for l in file.readlines():
        print(l.strip())

