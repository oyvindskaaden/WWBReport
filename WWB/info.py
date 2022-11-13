"""
Show Information,,,Customer Information,,
Venue:,Studentersamfundet,,Point of Contact:,Øyvind,
Address:,Gate nr 2
Po 2312321
3432, Sted 2 i norge
Trondheim, Trondheim   70302,,Address:,Adresse Linje 1
Linje 2
7213, Sted i Norge,
Phone:,12345,,Phone:,1234,
Fax:,67890,,Fax:,90,
E-mail:,samf@safsm.d,,E-mail:,email1@email.com,
Notes:,Notes test i dette programmet
Det viser seg at dette ikke funker?,,,,
"""


class Info(dict):
    def __init__(self):
        pass

    @classmethod
    def from_csv(cls,
            csv_lines   : list[str]  
        ):
        lines = [line.split(",") for line in csv_lines]
        
        return lines