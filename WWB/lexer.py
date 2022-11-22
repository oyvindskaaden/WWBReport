# Wireless Workbench Lexer

from datetime import datetime
from enum import Enum, auto
import json
from pygments.lexer import RegexLexer
from pygments.token import Token
import re
import pandas as pd

from . import channel as channel
from . import inclusion as inclusion
from . import exclusion as exclusion
from . import info as info


class CSVType(Enum):
    ACTIVE          = auto()
    BACKUP          = auto()
    USER_GROUP      = auto()
    INCLUSION_LIST  = auto()
    ACTIVE_TV       = auto()
    OTHER_EXCL      = auto()
    INFO            = auto()


class WWBLexer(RegexLexer):
    name                = 'WWBLex - Wireless Workbench Report file lexer'
    aliases             = ['wwb']
    filenames           = ['*.csv']

    wwb_tree        : dict  = {}
    current_zone    : dict  = {}
    current_group   : dict  = {}
    current_list    : list  = []

    current_list_state  : CSVType   = CSVType.ACTIVE
    has_read_header     : bool      = False

    def __register_showname_cb(self, match: re.Match):
        show_name = match.group(1)
        
        self.wwb_tree["show_name"]  : str       = show_name
        self.wwb_tree["info"]       : list[str] = []
        
        self.current_list           : list      = self.wwb_tree["info"]
        self.current_list_state     : CSVType   = CSVType.INFO
        self.has_read_header        : bool= False
        
        yield match.start(), Token.WWB.ShowName, show_name


    def __register_type_cb(self, match: re.Match):
        report_type                 : str       = match.group(1)
        
        self.wwb_tree["type"]       : str       = report_type
        
        yield match.start(), Token.WWB.Type, report_type


    def __register_rf_zone_cb(self, match: re.Match):
        if "zones" not in self.wwb_tree:
            self.wwb_tree["zones"]  : dict      = {}

        zone                        : str       = match.group(1)
        self.wwb_tree["zones"][zone]: dict      = {}
        self.current_zone           : dict = self.wwb_tree["zones"][zone]

        yield match.start(), Token.WWB.RFZone, zone


    def __register_active_cb(self, match: re.Match):
        no_active                   : int       = int(match.group(1))
        self.current_zone["active"] : dict      = {}
        
        self.current_zone["active"]["no_active"]    : int   = no_active

        self.current_group          : dict      = self.current_zone["active"]

        self.current_list_state     : CSVType   = CSVType.ACTIVE
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.ActiveChannels, "Active: " + str(no_active)
    

    def __register_backup_cb(self, match: re.Match):
        no_backup                   : int       = int(match.group(1))
        self.current_zone["backup"] : dict      = {}
        self.current_zone["backup"]["no_backup"]    : int   = no_backup

        self.current_group          : dict      = self.current_zone["backup"]

        self.current_list_state     : CSVType   = CSVType.BACKUP
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.ActiveChannel, "Backup: " + str(no_backup)

    def __register_group_cb(self, match: re.Match):
        inclusion_group             : str       = match.group(1)
        no_ch_in_group              : int       = int(match.group(2))

        self.current_group[inclusion_group] : list  = []
        self.current_list           : list      = self.current_group[inclusion_group]
        

        yield match.start(), Token.WWB.InclusionGroup, inclusion_group

    def __register_parameters_cb(self, match: re.Match):
        self.wwb_tree["parameters"] : dict      = {}
        
        yield match.start(), Token.WWB.Parameters, "Report Parameters"


    def __register_inclusions_cb(self, match: re.Match):
        self.wwb_tree["parameters"]["inclusions"]   : dict  = {}
        
        yield match.start(), Token.WWB.Inclusions, "Report Inclusions"
    

    def __register_user_group_cb(self, match: re.Match):
        user_group                  : str       = match.group(1)
        
        self.wwb_tree["parameters"]["inclusions"]["user_group_name"]    : str   = user_group
        self.wwb_tree["parameters"]["inclusions"]["user_group"]         : list  = []

        self.current_list           : list      = self.wwb_tree["parameters"]["inclusions"]["user_group"]
        self.current_list_state     : CSVType   = CSVType.USER_GROUP
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.UserGroup, user_group

    
    def __register_inclusion_list_cb(self, match: re.Match):
        user_group                  : str       = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list_name"]    : str   = user_group
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list"]         :list   = []

        self.current_list           : list      = self.wwb_tree["parameters"]["inclusions"]["inclusion_list"]
        self.current_list_state     : CSVType   = CSVType.INCLUSION_LIST
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.InclusionList, "Inclusion List"


    def __register_no_inclusions_cb(self, match: re.Match):
        group                       : str       = match.group(1)

        yield match.start, Token.WWB.NO_INCLUSION, "No " + group

    
    def __register_exclusions_cb(self, match: re.Match):
        self.wwb_tree["parameters"]["exclusions"]   : dict  = {}

        yield match.start(), Token.WWB.UserGroup, "Report Exclusions"


    def __register_active_tv_cb(self, match: re.Match):
        tv_channels                 : int       = int(match.group(1))

        self.wwb_tree["parameters"]["exclusions"]["no_active_tv"]   : int   = tv_channels
        self.wwb_tree["parameters"]["exclusions"]["active_tv"]      : list  = []

        self.current_list           : list      = self.wwb_tree["parameters"]["exclusions"]["active_tv"]
        self.current_list_state     : CSVType   = CSVType.ACTIVE_TV
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.TVChannels, "TV Channels: " + str(tv_channels)

    
    def __register_other_exlusions_cb(self, match: re.Match):
        no_other_exclusions         : int       = int(match.group(1))
        
        self.wwb_tree["parameters"]["exclusions"]["no_other_exlusions"] : int   = no_other_exclusions
        self.wwb_tree["parameters"]["exclusions"]["other_exlusions"]    : list  = []

        self.current_list           : list      = self.wwb_tree["parameters"]["exclusions"]["other_exlusions"]
        self.current_list_state     : CSVType   = CSVType.OTHER_EXCL
        self.has_read_header        : bool      = False

        yield match.start(), Token.WWB.OtherExclusions, "Other Exclusions: " + str(no_other_exclusions)


    def __register_date_created_cb(self, match: re.Match):
        time_format                 : str       = "%d %b %Y at %I:%M%p"
        created                     : datetime  = datetime.strptime(match.group(1), time_format)
        
        self.wwb_tree["created"]    : str       = created.isoformat()

        yield match.start(), Token.WWB.Created, "Created: " + created.isoformat()

    
    def __register_wwb_version_cb(self, match: re.Match):
        version                     : str       = match.group(1)
        
        self.wwb_tree["wwb_version"]: str       = version

        yield match.start(), Token.WWB.Version, version


    def __register_csv_cb(self, match: re.Match):
        csv_line                    : str       = match.group(0)

        if not csv_line:
            yield match.start(), Token.NEWLINE, "NEWLINE"
            return
        
        if not self.has_read_header:
            self.has_read_header    : bool  = True
            yield match.start(), Token.WWB.HEADER, "HEADER"
            return
        
        match self.current_list_state:
            case CSVType.ACTIVE:
                self.current_list.append(
                    channel.Active.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.CHANNEL.ACTIVE, csv_line

            case CSVType.BACKUP:
                self.current_list.append(
                    channel.Backup.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.CHANNEL.BACKUP, csv_line

            case CSVType.USER_GROUP:
                self.current_list.append(
                    inclusion.UserGroup.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.INCLUSION.USER_GROUP, csv_line

            case CSVType.INCLUSION_LIST:
                self.current_list.append(
                    inclusion.InclusionList.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.INCLUSION.LIST, csv_line

            case CSVType.ACTIVE_TV:
                self.current_list.append(
                    exclusion.ActiveTV.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.EXCLUSION.ACTIVE_TV, csv_line

            case CSVType.OTHER_EXCL:
                self.current_list.append(
                    exclusion.Other.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.EXCLUSION.OTHER, csv_line

            case CSVType.INFO:
                self.current_list.append(csv_line)
                yield match.start(), Token.WWB.INFO, csv_line

        return


    tokens = {
        'root': [
            (r'""\n"(.+)"\s+""',                    __register_showname_cb),

            (r'(?:""\n)?"(.* Report)"\s+',          __register_type_cb),

            (r'"RF Zone: (.+)"\s+',                 __register_rf_zone_cb),
            (r'"Active Channels \((\d+)\)"\s+',     __register_active_cb),
            (r'Backup Frequencies \((\d+)\),(?:Frequency List Source: (.+))?,\s+', 
                                                    __register_backup_cb),
            (r'\n(.+) \((\d+)\),{8}',               __register_group_cb),
            
            (r'""\n"Frequency Coordination Parameters"\s', 
                                                    __register_parameters_cb),
            
            (r'"Inclusions"\s+',                    __register_inclusions_cb),
            (r'"User Group List: (.+)"\s+',         __register_user_group_cb),
            (r'"Inclusion List: (.+)"\s+',          __register_inclusion_list_cb),
            (r'"No (.+) currently applied"',        __register_no_inclusions_cb),
            
            (r'"Exclusions"\s+',                    __register_exclusions_cb),
            (r'"Active TV Channels \((\d+)\)"\s+',  __register_active_tv_cb),
            (r'"Other Exclusions \((\d+)\)"\s+',    __register_other_exlusions_cb),
            
            (r'"Created on (.+ at .+)"\s+',         __register_date_created_cb),
            (r'"Generated using Wireless Workbench (.+)"\s+', 
                                                    __register_wwb_version_cb),
            (r'.+',                                 __register_csv_cb),

        ],
    }


    def __pre_process_wwb_string(self, wwb_string: str) -> str:
        """Preprocess the string, change wrong commas and change frequency decimal divider"""

        # Change the commas to dots for the frequency
        wwb_string                  : str       = re.sub(
            r'(\d{3}),(\d{3})',
            r'\1.\2',
            wwb_string
        )

        return wwb_string

    def get_wwb_tree(self, wwb_string: str) -> dict:
        # Pre process the string to fix issues with wwb format
        wwb_string                  : str       = self.__pre_process_wwb_string(wwb_string)
    
        # Lex the string and itterate trough to get the tree back
        lexed_wwb_report = self.get_tokens_unprocessed(wwb_string)
        for _, _, _ in lexed_wwb_report:
            continue

        if self.wwb_tree["info"]:
            self.wwb_tree["info"]   : info.Info = info.Info.from_csv(self.wwb_tree["info"])
        
        return self.wwb_tree


    def to_json(self, minimize: bool = True) -> str:
        return json.dumps(self.wwb_tree, ensure_ascii=False,indent= 4 if not minimize else None)

    
    def __str__(self) -> str:
        return self.to_json(minimize=False)
        

    