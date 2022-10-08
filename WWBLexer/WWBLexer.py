# Wireless Workbench Lexer

from datetime import datetime
from pygments.lexer import RegexLexer
from pygments.token import Token, Keyword, Generic



class WWBLexer(RegexLexer):
    name                = 'WWBLex - Wireless Workbench Report file lexer'
    aliases             = ['wwb']
    filenames           = ['*.csv']

    wwb_tree: dict      = {}
    current_csv: list   = []
    current_zone: dict = {}

    def register_showname_cb(self, match):
        self.wwb_tree["show_name"] = match.group(1)
        self.wwb_tree["contact_info"] = []
        self.current_csv = self.wwb_tree["contact_info"]

        print(f"Show name: {match.group(1)}")
        
        yield match.start(), Generic, "Show name"


    def register_type_cb(self, match):
        self.wwb_tree["type"] = match.group(1)
        yield match.start(), Generic, "Report Type"


    def register_rf_zone_cb(self, match):
        if "zones" not in self.wwb_tree:
                self.wwb_tree["zones"] = {}

        zone = match.group(1)
        self.wwb_tree["zones"][zone] = {}
        self.current_zone = self.wwb_tree["zones"][zone]

        yield match.start(), Generic, "RF Zone"


    def register_active_cb(self, match):
        self.current_zone["no_active"] = match.group(1)
        self.current_zone["active"] = []

        self.current_csv = self.current_zone["active"]

        yield match.start(), Generic, "Active channels"
    

    def register_backup_cb(self, match):
        self.current_zone["no_backup"] = match.group(1)
        self.current_zone["backup"] = []

        self.current_csv = self.current_zone["backup"]

        yield match.start(), Generic, "Backup channels"


    def register_parameters_cb(self, match):
        self.wwb_tree["parameters"] = {}
        yield match.start(), Generic, "Report Parameters"


    def register_inclusions_cb(self, match):
        self.wwb_tree["parameters"]["inclusions"] = {}
        yield match.start(), Generic, "Report Inclusions"
    

    def register_user_group_cb(self, match):
        self.wwb_tree["parameters"]["inclusions"]["user_group_name"] = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["user_group"] = []
        self.current_csv = self.wwb_tree["parameters"]["inclusions"]["user_group"]

        yield match.start(), Generic, "User group"

    
    def register_inclusion_list_cb(self, match):
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list_name"] = match.group(1)
        self.wwb_tree["parameters"]["inclusions"]["inclusion_list"] = []
        self.current_csv = self.wwb_tree["parameters"]["inclusions"]["inclusion_list"]

        yield match.start(), Generic, "Inclusion List"

    
    def register_exclusions_cb(self, match):
        self.wwb_tree["parameters"]["exclusions"] = {}

        yield match.start(), Generic, "Report Exclusions"


    def register_active_tv_cb(self, match):
        self.wwb_tree["parameters"]["exclusions"]["no_active_tv"] = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["active_tv"] = []
        self.current_csv = self.wwb_tree["parameters"]["exclusions"]["active_tv"]

        yield match.start(), Generic, "Active TV channels"

    
    def register_other_exlusions_cb(self, match):
        self.wwb_tree["parameters"]["exclusions"]["no_other_exlusions"] = match.group(1)
        self.wwb_tree["parameters"]["exclusions"]["other_exlusions"] = []
        self.current_csv = self.wwb_tree["parameters"]["exclusions"]["other_exlusions"]

        yield match.start(), Generic, "Other Exclusions"

    def register_date_created_cb(self, match):
        time_format = "%d %b %Y at %I:%M%p"
        created = datetime.strptime(match.group(1), time_format)
        self.wwb_tree["created"] = created.isoformat()

        yield match.start(), Generic, created

    
    def register_wwb_version_cb(self, match):
        version = match.group(1)
        self.wwb_tree["wwb_version"] = version

        yield match.start(), Generic, version


    def register_csv_cb(self, match):
        self.current_csv.append(match.group(0))
        yield match.start(), Generic, "CSV"


    tokens = {
        'root': [
            (r'""\n"(.+)"\s+""',                    register_showname_cb),

            (r'""\n"(.* Report)"\s+',               register_type_cb),

            (r'"RF Zone: (.+)"\s+',                 register_rf_zone_cb),
            (r'"Active Channels \((\d+)\)"\s+',     register_active_cb),
            (r'Backup Frequencies \((\d+)\),(?:Frequency List Source: (.+))?,\s+', 
                                                    register_backup_cb),
            
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
            
            (r'(.*,)',                          register_csv_cb)
        ],

    }

    
    def get_wwb_tree(self):
        return self.wwb_tree