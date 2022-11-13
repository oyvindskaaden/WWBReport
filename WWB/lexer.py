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


class CSVType(Enum):
    ACTIVE          = auto()
    BACKUP          = auto()
    USER_GROUP      = auto()
    INCLUSION_LIST  = auto()
    ACTIVE_TV       = auto()
    OTHER_EXCL      = auto()


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
        
        self.wwb_tree["show_name"] = show_name
        self.wwb_tree["contact_info"] = []
        self.current_list = self.wwb_tree["contact_info"]
        self.has_read_header = False
        
        yield match.start(), Token.WWB.ShowName, show_name


    def __register_type_cb(self, match: re.Match):
        report_type = match.group(1)
        self.wwb_tree["type"] = report_type
        yield match.start(), Token.WWB.Type, report_type


    def __register_rf_zone_cb(self, match: re.Match):
        if "zones" not in self.wwb_tree:
                self.wwb_tree["zones"] = {}

        zone = match.group(1)
        self.wwb_tree["zones"][zone] = {}
        self.current_zone = self.wwb_tree["zones"][zone]

        yield match.start(), Token.WWB.RFZone, zone


    def __register_active_cb(self, match: re.Match):
        no_channels = match.group(1)
        self.current_zone["active"] = {}
        self.current_zone["active"]["no_active"] = no_channels

        self.current_group = self.current_zone["active"]

        yield match.start(), Token.WWB.ActiveChannels, no_channels
    

    def __register_backup_cb(self, match: re.Match):
        no_backup = match.group(1)
        self.current_zone["backup"] = {}
        self.current_zone["backup"]["no_backup"] = no_backup

        self.current_group = self.current_zone["backup"]

        yield match.start(), Token.WWB.ActiveChannel, no_backup

    def __register_group_cb(self, match: re.Match):
        inclusion_group = match.group(1)
        no_ch_in_group = match.group(2)

        self.current_group[inclusion_group] = []
        self.current_list = self.current_group[inclusion_group]
        self.has_read_header = False

        yield match.start(), Token.WWB.InclusionGroup, inclusion_group

    def __register_parameters_cb(self, match: re.Match):
        self.wwb_tree["parameters"] = {}
        yield match.start(), Token.WWB.Parameters, "Report Parameters"


    def __register_inclusions_cb(self, match: re.Match):
        self.wwb_tree["parameters"]["inclusions"] = {}
        yield match.start(), Token.WWB.Inclusions, "Report Inclusions"
    

    def __register_user_group_cb(self, match: re.Match):
        user_group  : str   = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["user_group_name"] = user_group
        self.wwb_tree["parameters"]["inclusions"]["user_group"] = []
        self.current_list = self.wwb_tree["parameters"]["inclusions"]["user_group"]
        self.has_read_header = False

        yield match.start(), Token.WWB.UserGroup, user_group

    
    def __register_inclusion_list_cb(self, match: re.Match):
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list_name"] = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list"] = []
        self.current_list = self.wwb_tree["parameters"]["inclusions"]["inclusion_list"]
        self.has_read_header = False

        yield match.start(), Token.WWB.InclusionList, "Inclusion List"

    
    def __register_exclusions_cb(self, match: re.Match):
        self.wwb_tree["parameters"]["exclusions"] = {}

        yield match.start(), Token.WWB.UserGroup, "Report Exclusions"


    def __register_active_tv_cb(self, match: re.Match):
        tv_channels = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["no_active_tv"] = tv_channels
        self.wwb_tree["parameters"]["exclusions"]["active_tv"] = []
        self.current_list = self.wwb_tree["parameters"]["exclusions"]["active_tv"]
        self.has_read_header = False

        yield match.start(), Token.WWB.TVChannels, tv_channels

    
    def __register_other_exlusions_cb(self, match: re.Match):
        other_exclusions = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["no_other_exlusions"] = other_exclusions
        self.wwb_tree["parameters"]["exclusions"]["other_exlusions"] = []
        self.current_list = self.wwb_tree["parameters"]["exclusions"]["other_exlusions"]
        self.has_read_header = False

        yield match.start(), Token.WWB.OtherExclusions, other_exclusions


    def __register_date_created_cb(self, match: re.Match):
        time_format = "%d %b %Y at %I:%M%p"
        created = datetime.strptime(match.group(1), time_format)
        self.wwb_tree["created"] = created.isoformat()

        yield match.start(), Token.WWB.Created, created.isoformat()

    
    def __register_wwb_version_cb(self, match: re.Match):
        version = match.group(1)
        self.wwb_tree["wwb_version"] = version

        yield match.start(), Token.WWB.Version, version


    def __register_csv_cb(self, match: re.Match):
        csv_line = match.group(0)#.split(',')
        
        # if "header" not in self.current_group:
        #     self.current_group["header"] = csv_line
        # else:
        #     self.current_list.append(csv_line)
        if not self.has_read_header:
            self.has_read_header = True
            yield match.start(), Token.WWB.HEADER, "HEADER"
            return
        


        match self.current_list_state:
            case CSVType.ACTIVE:
                self.current_list.append(
                    channel.Active.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.CHANNEL.ACTIVE, "ACTIVE CH"

            case CSVType.BACKUP:
                self.current_list.append(
                    channel.Backup.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.CHANNEL.BACKUP, "BACKUP CH"

            case CSVType.USER_GROUP:
                self.current_list.append(
                    inclusion.UserGroup.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.INCLUSION.USER_GROUP, "USER GROUP INCL"

            case CSVType.INCLUSION_LIST:
                self.current_list.append(
                    inclusion.InclusionList.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.INCLUSION.LIST, "INCLUSION LIST"

            case CSVType.ACTIVE_TV:
                self.current_list.append(
                    exclusion.ActiveTV.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.EXCLUSION.ACTIVE_TV, "ACTIVE_TV EXCL"

            case CSVType.OTHER_EXCL:
                self.current_list.append(
                    exclusion.Active.from_csvrow(csv_line)
                )
                yield match.start(), Token.WWB.EXCLUSION.OTHER, "OTHER EXCL"

        
        return


    tokens = {
        'root': [
            (r'""\n"(.+)"\s+""',                    __register_showname_cb),

            (r'"(.* Report)"\s+',                   __register_type_cb),

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
            
            (r'"Exclusions"\s+',                    __register_exclusions_cb),
            (r'"Active TV Channels \((\d+)\)"\s+',  __register_active_tv_cb),
            (r'"Other Exclusions \((\d+)\)"\s+',    __register_other_exlusions_cb),
            
            (r'"Created on (.+ at .+)"\s+',         __register_date_created_cb),
            (r'Generated using Wireless Workbench (.+)"\s+', 
                                                    __register_wwb_version_cb),
            
            (r'(.*,)',                              __register_csv_cb)
        ],
    }

    def __to_dataframe(self, csv_list: list[str]):
        csv_list = pd.read_csv(csv_list)

    def __pre_process_wwb_string(self, wwb_string: str) -> str:
        """Preprocess the string, change wrong commas and change frequency decimal divider"""
        
        # Change the commas in the TV channel lists
        wwb_string = wwb_string.replace(", ", ";")

        # Change the commas to dots for the frequency
        wwb_string = re.sub(r'(\d{3}),(\d{3})',
                            r'\1.\2',
                            wwb_string)
        return wwb_string

    def __generate_info_dict(self, data_src: pd.DataFrame, data_target_key: str, location: list) -> None:
        self.wwb_tree["contact_info"][data_target_key] = {}
        for _, row in data_src.iloc[:,location].copy().iterrows():
            if not row[location[0]]:
                continue
            self.wwb_tree["contact_info"][data_target_key][row[location[0]].replace(":", "")] = row[location[1]]
        return

    def __post_process_wwb_tree(self) -> None:

        if self.wwb_tree["contact_info"]:
            #self.wwb_tree["contact_info_show"] = pd.DataFrame(
            show_info: pd.DataFrame = pd.DataFrame(
                self.wwb_tree["contact_info"]#[1:],
                #columns=self.wwb_tree["contact_info_show"][0]
            )

            self.wwb_tree["contact_info"] = {}

            self.__generate_info_dict(show_info, "show", [0,1])
            self.__generate_info_dict(show_info, "customer", [3,4])

        #for index, row in self.wwb_tree["contact_info_show"].iloc[:,[3,4]].copy().iterrows():
        #    print(row[3].replace(":", "") , row[4])

        #self.wwb_tree["contact_info_customer"] = self.wwb_tree["contact_info_show"].iloc[:,[3,4]].copy().to_dict()
        #self.wwb_tree["contact_info_show"] = self.wwb_tree["contact_info_show"].iloc[:,[0,1]].copy().to_dict()

        # for zone in self.wwb_tree["zones"]:
        #     for type in self.wwb_tree["zones"][zone]:
        #         for group in self.wwb_tree["zones"][zone][type]:
        #             if group == "header" or group.startswith("no_"):
        #                 continue
                    
        #             if not self.wwb_tree["zones"][zone][type][group]:
        #                 continue

        #             # Move the Frequency header from GroupChannel to actual frequency.
        #             header = self.wwb_tree["zones"][zone][type]["header"]

        #             # Group frequency is in column 4 (5) and the actual frequencies is in 5 (6)
        #             header[4] = ""
        #             header[5] = "Frequency"

        #             # Create dataframe with the new custom header.
        #             # Using the same header over for multiple rf zones
        #             df = pd.DataFrame(
        #                 self.wwb_tree["zones"][zone][type][group],
        #                 columns=header
        #             )
                    
        #             # Drop the empty columns
        #             df.drop("", axis="columns", inplace=True)
                    
        #             self.wwb_tree["zones"][zone][type][group] = df.to_dict()
                
        #         if "header" not in self.wwb_tree["zones"][zone][type]:
        #             continue
        #         self.wwb_tree["zones"][zone][type].pop("header")


        # for params in self.wwb_tree["parameters"]:
        #     for param in self.wwb_tree["parameters"][params]:
        #         if param.startswith('no_') or param.endswith('_name'):
        #             continue

        #         if not self.wwb_tree["parameters"][params][param]:
        #             continue
        #         df = pd.DataFrame(
        #             self.wwb_tree["parameters"][params][param][1:],
        #             columns=self.wwb_tree["parameters"][params][param][0]
        #         )
                
        #         # Drop the empty columns
        #         df.drop("", axis="columns", inplace=True)

        #         self.wwb_tree["parameters"][params][param] = df.to_dict()
        return

    

    def get_wwb_tree(self, wwb_string: str, post_process: bool = True) -> dict:
        # Pre process the string to fix issues with wwb format
        wwb_string = self.__pre_process_wwb_string(wwb_string)
    
        # Lex the string and itterate trough to get the tree back
        lexed_wwb_report = self.get_tokens_unprocessed(wwb_string)
        for _, _, _ in lexed_wwb_report:
            continue


        if post_process:
            self.__post_process_wwb_tree()
        
        return self.wwb_tree


    def to_json(self, minimize: bool = True) -> str:
        return json.dumps(self.wwb_tree, indent= 4 if not minimize else None)

    
    def __str__(self) -> str:
        return self.to_json(minimize=False)
        

    