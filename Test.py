#!/usr/bin/env python3

from wwb.channel import Channel
from wwb.backup import Backup
import json


test = {
    "channel":  Channel.from_csvrow("AD4D-A,G56,Shure,[AD4D-A],G:-- Ch:--,552.075 MHz,Tag Test 1,Tag Test 2,,"),
    "backup":   Backup.from_csvrow("AD/Standard,G56,,,G:-- Ch:--,615,100 MHz,,,")
}


print(json.dumps(test, indent=2))