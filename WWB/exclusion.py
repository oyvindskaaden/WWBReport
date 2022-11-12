import json

class ActiveTV(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            type            : str,
            channels        : list[str]
        ) -> None:
        """
        Form a WWB Active TV Exclusions Object from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["type"]            : str       = type
        self["channels"]        : list[str] = channels

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB Channel Object from a csv row on the following format:

        `Type,[Channels]*,,,,`
        """

        fields  = csv_line.split(",")

        # The csv string is as follows
        # Model, Band, Channel Name, Device ID, Channel/Group, Frequency, [Tags]*,,
        type            : str       = fields.pop(0)     # Model field
        channels        : list[str] = fields[:-4]       # The rest, but not the last 2, are tags

        return cls(type, [channel.strip() for channel in channels])


    ################
    ## PROPERTIES ##
    ################
    @property
    def type(self) -> str:
        return self["type"]
    
    @property
    def channels(self) -> list[str]:
        return self["channels"]
    

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"Type:          {self.type}\n"
        cls_str += f"Channels:      {self.channels}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)


class Other(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            type            : str,
            source          : str,
            frequency       : list[str],
            notes           : str
        ) -> None:
        """type, source, frequency, notes
        Form a WWB Other Exclusions Object from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["type"]            : str       = type
        self["source"]          : str       = source
        self["frequency"]       : list[str] = frequency
        self["notes"]           : str       = notes

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB Channel Object from a csv row on the following format:

        `Type,Source,Frequency,Notes,,`
        """

        fields  = csv_line.split(",")

        # The csv string is as follows
        # Type,Source,Frequency,Notes,,
        # Frequency can be single, or a range on the format "000.000 MHz - 000.000 MHz"
        type            : str       = fields.pop(0)                 # Model field
        source          : str       = fields.pop(0)                 # Source field
        frequency       : list[str] = fields.pop(0).split(" - ")    # Model field
        notes           : str       = fields.pop(0)                 # Model field
        
        return cls(type, source, frequency, notes)


    ################
    ## PROPERTIES ##
    ################
    @property
    def type(self) -> str:
        return self["type"]

    @property
    def source(self) -> str:
        return self["source"]
    
    @property
    def frequency(self) -> list[str]:
        return self["frequency"]
    
    @property
    def notes(self) -> str:
        return self["notes"]

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"Type:          {self.type}\n"
        cls_str  = f"Source:        {self.source}\n"
        cls_str += f"Frequency:     {self.frequency}\n"
        cls_str += f"Notes:         {self.notes}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)