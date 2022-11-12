#!/usr/bin/env python3

import WWB.WWBChannel as WWB
import json

test = WWB.Channel.from_csvrow("AD4D-A,G56,Shure,[AD4D-A],G:-- Ch:--,552.075 MHz,Tag Test 1,Tag Test 2,,")

print(test)

test["model"] = "Test"


print(json.dumps(test, indent=4))