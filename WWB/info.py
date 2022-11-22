import json
from pprint import pprint
import re

class Info(dict):
    def __init__(self,
            venue_name      : str,
            venue_address   : list[str],
            venue_phone     : str,
            venue_fax       : str,
            venue_email     : str,

            contact_name    : str,
            contact_address : list[str],
            contact_phone   : str,
            contact_fax     : str,
            contact_email   : str,
            
            notes           : list[str]
        ):
        self["venue"] = {
            "name": venue_name,
            "address": venue_address,
            "phone": venue_phone,
            "fax": venue_fax,
            "email": venue_email
        }

        self["contact"] = {
            "name": contact_name,
            "address": contact_address,
            "phone": contact_phone,
            "fax": contact_fax,
            "email": contact_email
        }
        
        self["notes"] = notes


        for t in ["venue", "contact"]:
            empty = True
            for k in self[t]:
                empty = False if self[t][k] else empty
            if empty:
                del self[t]

        # if empty:
        #     del self["contact"]
        #     del self["venue"]
        #     del self["notes"]


    @classmethod
    def from_dict(cls,
            info_dict   : dict
        ):
        return cls(
            info_dict["venue"]["name"],
            info_dict["venue"]["address"],
            info_dict["venue"]["phone"],
            info_dict["venue"]["fax"],
            info_dict["venue"]["email"],
            
            info_dict["contact"]["name"],
            info_dict["contact"]["address"],
            info_dict["contact"]["phone"],
            info_dict["contact"]["fax"],
            info_dict["contact"]["email"],

            info_dict["notes"] 
        )

    @classmethod
    def from_csv(cls,
            csv_lines   : list[str]  
        ):
        lines   : list[list[str]]= [line.split(",") for line in csv_lines]

        info = {}
        info["venue"] = {}
        info["contact"] = {}

        multiline_start_index   = -1

        lines_to_delete : list[int] = []

        for i, line in enumerate(lines):
            if (not re.match(r"[\w-]+:", line[0])):
                lines_to_delete.append(i)
                if "Address:" in line:
                    lines[multiline_start_index] += line
                else:
                    lines[multiline_start_index].append(",".join(line))
            else:
                multiline_start_index   = i

        lines_to_delete.reverse()
        for i in lines_to_delete:
            lines.pop(i)

        for i, line in enumerate(lines):
            # print(i, line)
            match line[0]: 
                case "Venue:":
                    info["venue"]["name"]       : str       = line[1]
                    info["contact"]["name"]     : str       = line[4]
                    pass
                case "Address:":
                    indices = [i for i, _ in enumerate(line) if _ == "Address:"]

                    venue_address   : list[str] = [
                        item.strip() for sublist in [s.rstrip(",").split("   ") for s in line[indices[0] + 1:indices[1] - 1]] for item in sublist
                    ]
                    contact_address : list[str] = [s.rstrip(",") for s in line[indices[1] + 1:]]

                    # Remove empty lines
                    venue_address   : list[str] = remove_lead_trail(venue_address)
                    contact_address : list[str] = remove_lead_trail(contact_address)
                    
                    # Guess what should be commas
                    lines_to_delete : list[int] = []
                    for i, l in enumerate(venue_address):
                        if l[0].islower() and len(venue_address) > 1:
                            venue_address[i - 1] += ", " + l
                            lines_to_delete.append(i)
                    
                    lines_to_delete.reverse()
                    for i in lines_to_delete:
                        venue_address.pop(i)

                    info["venue"]["address"]    : list[str] = venue_address
                    info["contact"]["address"]  : list[str] = contact_address
                    pass
                case "Phone:":
                    info["venue"]["phone"]      : str       = line[1]
                    info["contact"]["phone"]    : str       = line[4]
                    pass
                case "Fax:":
                    info["venue"]["fax"]        : str       = line[1]
                    info["contact"]["fax"]      : str       = line[4]
                    pass
                case "E-mail:":
                    info["venue"]["email"]      : str       = line[1]
                    info["contact"]["email"]    : str       = line[4]
                    pass
                case "Notes:":
                    notes                       : str       = [s.rstrip(",") for s in line[1:]]
                    notes                       : str       = remove_lead_trail(notes)
                    info["notes"]               : str       = notes
                    pass
        
        return cls.from_dict(info_dict=info)

    ################
    ## PROPERTIES ##
    ################
    @property
    def venue(self) -> dict:
        return self["venue"]
    @property
    def venue_name(self) -> str:
        return self["venue"]["name"]
    @property
    def venue_address(self) -> list[str]:
        return self["venue"]["address"]
    @property
    def venue_phone(self) -> str:
        return self["venue"]["phone"]
    @property
    def venue_fax(self) -> str:
        return self["venue"]["fax"]
    @property
    def venue_email(self) -> str:
        return self["venue"]["email"]
    
    
    @property
    def contact(self) -> dict:
        return self["contact"]
    @property
    def contact_name(self) -> str:
        return self["contact"]["name"]
    @property
    def contact_address(self) -> list[str]:
        return self["contact"]["address"]
    @property
    def contact_phone(self) -> str:
        return self["contact"]["phone"]
    @property
    def contact_fax(self) -> str:
        return self["contact"]["fax"]
    @property
    def contact_email(self) -> str:
        return self["contact"]["email"]
    

    @property
    def notes(self) -> list[str]:
        return self["notes"]

    @property
    def header(self) -> str:
        return ["Name", "Address", "Phone", "Fax", "E-mail"]

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"Venue Name:        {self.venue_name}\n"
        cls_str += f"Venue Address:     {self.venue_address}\n"
        cls_str += f"Venue Phone:       {self.venue_phone}\n"
        cls_str += f"Venue Fax:         {self.venue_fax}\n"
        cls_str += f"Venue E-Mail:      {self.venue_email}\n"
        cls_str += "\n"
        cls_str  = f"Contact Name:      {self.contact_name}\n"
        cls_str += f"Contact Address:   {self.contact_address}\n"
        cls_str += f"Contact Phone:     {self.contact_phone}\n"
        cls_str += f"Contact Fax:       {self.contact_fax}\n"
        cls_str += f"Contact E-Mail:    {self.contact_phone}\n"

        cls_str += f"Notes:             {self.notes}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)

def remove_lead_trail(l: list):
    """Removes leading and trailing falsy values from the list"""
    while l and not l[0]:
        l.pop(0)
    while l and not l[-1]:
        l.pop()
    return l