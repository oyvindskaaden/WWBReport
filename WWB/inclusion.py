import json

class UserGroup(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            user_group      : str,
            type            : str,
            frequency       : str,
            tv              : str
        ) -> None:
        """
        Form a WWB User Group Inclusion Object from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["user_group"]      : str       = user_group
        self["type"]            : str       = type
        self["frequency"]       : list[str] = frequency
        self["tv"]              : str       = tv

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB User Group Inclusion from a csv row on the following format:

        `User Group,Type,Frequency,TV,,`
        """

        fields  = csv_line.split(",")

        # The csv string is as follows
        # User Group,Type,Frequency,TV,,
        # Frequency can be single, or a range on the format "000.000 MHz - 000.000 MHz"
        user_group      : str       = fields.pop(0)                 # Model field
        type            : str       = fields.pop(0)                 # Band field
        frequency       : list[str] = fields.pop(0).split(" - ")    # Frequency field
        tv              : str       = fields.pop(0)                 # The rest, but not the last 2, are tags

        return cls(user_group, type, frequency, tv)


    ################
    ## PROPERTIES ##
    ################
    @property
    def user_group(self) -> str:
        return self["user_group"]
    
    @user_group.setter
    def user_group(self, value: str) -> None:
        self["user_group"]  = value

    @property
    def type(self) -> str:
        return self["type"]

    @property
    def frequency(self) -> list[str]:
        return self["frequency"]
    
    @property
    def tags(self) -> list[str]:
        return self["tags"]
    

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"User group:    {self.user_group}\n"
        cls_str += f"Type:          {self.type}\n"
        cls_str += f"Frequency:     {self.frequency}\n"
        cls_str += f"TV Channels:   {self.tags}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)

    
class InclusionList(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            inclusion_group : str,
            type            : str,
            frequency       : str,
            tv              : str
        ) -> None:
        """
        Form a WWB WWB Inclusion List from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["inclusion_group"] : str       = inclusion_group
        self["type"]            : str       = type
        self["frequency"]       : list[str] = frequency
        self["tv"]              : str       = tv

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB User Group Inclusion from a csv row on the following format:

        `Inclusion Group,Type,Frequency,TV,,`
        """

        fields  = csv_line.split(",")

        # The csv string is as follows
        # Inclusion Group,Type,Frequency,TV,,
        # Frequency can be single, or a range on the format "000.000 MHz - 000.000 MHz"
        inclusion_group : str       = fields.pop(0)                 # Model field
        type            : str       = fields.pop(0)                 # Band field
        frequency       : list[str] = fields.pop(0).split(" - ")    # Frequency field
        tv              : str       = fields.pop(0)                 # The rest, but not the last 2, are tags

        return cls(inclusion_group, type, frequency, tv)


    ################
    ## PROPERTIES ##
    ################
    @property
    def inclusion_group(self) -> str:
        return self["inclusion_group"]
    
    @inclusion_group.setter
    def inclusion_group(self, value: str) -> None:
        self["inclusion_group"]  = value

    @property
    def type(self) -> str:
        return self["type"]

    @property
    def frequency(self) -> list[str]:
        return self["frequency"]
    
    @property
    def tags(self) -> list[str]:
        return self["tags"]
    

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"Inclusion group:   {self.inclusion_group}\n"
        cls_str += f"Type:              {self.type}\n"
        cls_str += f"Frequency:         {self.frequency}\n"
        cls_str += f"TV Channels:       {self.tags}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)