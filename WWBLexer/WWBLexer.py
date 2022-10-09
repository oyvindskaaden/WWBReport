# Wireless Workbench Lexer

from datetime import datetime
from pygments.lexer import RegexLexer
from pygments.token import Token, Keyword, Generic
import re


class WWBLexer(RegexLexer):
    name                = 'WWBLex - Wireless Workbench Report file lexer'
    aliases             = ['wwb']
    filenames           = ['*.csv']

    wwb_tree: dict      = {}
    current_csv: list   = []
    current_zone: dict  = {}

    def register_showname_cb(self: RegexLexer, match: re.Match):
        show_name = match.group(1)
        
        self.wwb_tree["show_name"] = show_name
        self.wwb_tree["contact_info"] = []
        self.current_csv = self.wwb_tree["contact_info"]
        
        yield match.start(), Token.WWB.ShowName, show_name


    def register_type_cb(self: RegexLexer, match: re.Match):
        report_type = match.group(1)
        self.wwb_tree["type"] = report_type
        yield match.start(), Token.WWB.Type, report_type


    def register_rf_zone_cb(self: RegexLexer, match: re.Match):
        if "zones" not in self.wwb_tree:
                self.wwb_tree["zones"] = {}

        zone = match.group(1)
        self.wwb_tree["zones"][zone] = {}
        self.current_zone = self.wwb_tree["zones"][zone]

        yield match.start(), Token.WWB.RFZone, zone


    def register_active_cb(self: RegexLexer, match: re.Match):
        no_channels = match.group(1)
        self.current_zone["no_active"] = no_channels
        self.current_zone["active"] = []

        self.current_csv = self.current_zone["active"]

        yield match.start(), Token.WWB.ActiveChannels, no_channels
    

    def register_backup_cb(self: RegexLexer, match: re.Match):
        no_backup = match.group(1)
        self.current_zone["no_backup"] = no_backup
        self.current_zone["backup"] = []

        self.current_csv = self.current_zone["backup"]

        yield match.start(), Token.WWB.ActiveChannel, no_backup

    def register_group_cb(self: RegexLexer, match: re.Match):
        inclusion_group = match.group(1)
        no_ch_in_group = match.group(2)
        yield match.start(), Token.WWB.InclusionGroup, inclusion_group

    def register_parameters_cb(self: RegexLexer, match: re.Match):
        self.wwb_tree["parameters"] = {}
        yield match.start(), Token.WWB.Parameters, "Report Parameters"


    def register_inclusions_cb(self: RegexLexer, match: re.Match):
        self.wwb_tree["parameters"]["inclusions"] = {}
        yield match.start(), Token.WWB.Inclusions, "Report Inclusions"
    

    def register_user_group_cb(self: RegexLexer, match: re.Match):
        user_group = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["user_group_name"] = user_group
        self.wwb_tree["parameters"]["inclusions"]["user_group"] = []
        self.current_csv = self.wwb_tree["parameters"]["inclusions"]["user_group"]

        yield match.start(), Token.WWB.UserGroup, user_group

    
    def register_inclusion_list_cb(self: RegexLexer, match: re.Match):
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list_name"] = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list"] = []
        self.current_csv = self.wwb_tree["parameters"]["inclusions"]["inclusion_list"]

        yield match.start(), Token.WWB.InclusionList, "Inclusion List"

    
    def register_exclusions_cb(self: RegexLexer, match: re.Match):
        self.wwb_tree["parameters"]["exclusions"] = {}

        yield match.start(), Token.WWB.UserGroup, "Report Exclusions"


    def register_active_tv_cb(self: RegexLexer, match: re.Match):
        tv_channels = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["no_active_tv"] = tv_channels
        self.wwb_tree["parameters"]["exclusions"]["active_tv"] = []
        self.current_csv = self.wwb_tree["parameters"]["exclusions"]["active_tv"]

        yield match.start(), Token.WWB.TVChannels, tv_channels

    
    def register_other_exlusions_cb(self: RegexLexer, match: re.Match):
        other_exclusions = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["no_other_exlusions"] = other_exclusions
        self.wwb_tree["parameters"]["exclusions"]["other_exlusions"] = []
        self.current_csv = self.wwb_tree["parameters"]["exclusions"]["other_exlusions"]

        yield match.start(), Token.WWB.OtherExclusions, other_exclusions


    def register_date_created_cb(self: RegexLexer, match: re.Match):
        time_format = "%d %b %Y at %I:%M%p"
        created = datetime.strptime(match.group(1), time_format)
        self.wwb_tree["created"] = created.isoformat()

        yield match.start(), Token.WWB.Created, created.isoformat()

    
    def register_wwb_version_cb(self: RegexLexer, match: re.Match):
        version = match.group(1)
        self.wwb_tree["wwb_version"] = version

        yield match.start(), Token.WWB.Version, version


    def register_csv_cb(self: RegexLexer, match: re.Match):
        self.current_csv.append(match.group(0))
        yield match.start(), Token.WWB.CSV, "CSV"


    tokens = {
        'root': [
            (r'""\n"(.+)"\s+""',                    register_showname_cb),

            (r'""\n"(.* Report)"\s+',               register_type_cb),

            (r'"RF Zone: (.+)"\s+',                 register_rf_zone_cb),
            (r'"Active Channels \((\d+)\)"\s+',     register_active_cb),
            (r'Backup Frequencies \((\d+)\),(?:Frequency List Source: (.+))?,\s+', 
                                                    register_backup_cb),
            (r'\n(.+) \((\d+)\),{8}',               register_group_cb),
            
            (r'""\n"Frequency Coordination Parameters"\s', 
                                                    register_parameters_cb),
            
            (r'"Inclusions"\s+',                    register_inclusions_cb),
            (r'"User Group List: (.+)"\s+',         register_user_group_cb),
            (r'"Inclusion List: (.+)"\s+',          register_inclusion_list_cb),
            
            (r'"Exclusions"\s+',                    register_exclusions_cb),
            (r'"Active TV Channels \((\d+)\)"\s+',  register_active_tv_cb),
            (r'"Other Exclusions \((\d+)\)"\s+',    register_other_exlusions_cb),
            
            (r'"Created on (.+ at .+)"\s+',         register_date_created_cb),
            (r'Generated using Wireless Workbench (.+)"\s+', 
                                                    register_wwb_version_cb),
            
            (r'(.*,)',                              register_csv_cb)
        ],

    }