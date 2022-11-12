#!/usr/bin/env python3

import wwb.channel as channel
import wwb.inclusion as inclusion
import wwb.exclusion as exclusion
import json


test = {
    "channel":      channel.Active.from_csvrow("AD4D-A,G56,Shure,[AD4D-A],G:-- Ch:--,552.075 MHz,Tag Test 1,Tag Test 2,,"),
    "backup":       channel.Backup.from_csvrow("AD/Standard,G56,,,G:-- Ch:--,615,100 MHz,,,"),
    "user_inc_1":   inclusion.UserGroup.from_csvrow("Australia Indoors,Range,1786.000 MHz - 1800.000 MHz,,,"),
    "user_inc_2":   inclusion.UserGroup.from_csvrow(",Single,567.250 MHz,,,"),
    "inc_list_1":   inclusion.InclusionList.from_csvrow("Group 2,Range,223.168 MHz - 224.704 MHz,12A,,"),
    "inc_list_2":   inclusion.InclusionList.from_csvrow(",Range,566.000 MHz - 636.000 MHz,,,"),
    "ex_tv"     :   exclusion.ActiveTV.from_csvrow("Digital Audio,10A, 10B, 10C, 10D, 10N, 11A, 11B, 11C, 11D, 11N, 12A, 12B, 12C, 12D, 12N, 5A, 5B, 5C, 5D, 6A, 6B, 6C, 6D, 7A, 7B, 7C, 7D, 8A, 8B, 8C, 8D, 9A, 9B, 9C, 9D,,,,"),
    "other_ex_1":   exclusion.Other.from_csvrow("Single,Manual,543.350 MHz,,,"),
    "other_ex_2":   exclusion.Other.from_csvrow("Range,Manual,734.000 MHz - 738.000 MHz,Test Lower,,")
}



print(json.dumps(test, indent=2))