import json

class Active(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            model           : str,
            band            : str,
            channel_name    : str,
            device_id       : str,
            frequency       : str,
            tags            : list[str]
        ) -> None:
        """
        Form a WWB Channel Object from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["model"]           : str       = model
        self["band"]            : str       = band
        self["channel_name"]    : str       = channel_name
        self["device_id"]       : str       = device_id
        self["frequency"]       : str       = frequency
        self["tags"]            : list[str] = tags

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB Channel Object from a csv row on the following format:

        `Model, Band, Channel Name, Device ID, Channel/Group, Frequency, [Tags]*,,`
        """
        fields  = csv_line.split(",")

        # The csv string is as follows
        # Model, Band, Channel Name, Device ID, Channel/Group, Frequency, [Tags]*,,
        model           : str       = fields.pop(0)     # Model field
        band            : str       = fields.pop(0)     # Band field
        channel_name    : str       = fields.pop(0)     # Channel name field
        device_id       : str       = fields.pop(0)     # Device ID field
        _                           = fields.pop(0)     # This field is unused, the Channel/Group
        frequency       : str       = fields.pop(0)     # Frequency field
        tags            : list[str] = fields[:-2]       # The rest, but not the last 2, are tags

        return cls(model, band, channel_name, device_id, frequency, tags)


    ################
    ## PROPERTIES ##
    ################
    @property
    def model(self) -> str:
        return self["model"]

    @property
    def band(self) -> str:
        return self["band"]

    @property
    def channel_name(self) -> str:
        return self["channel_name"]

    @property
    def device_id(self) -> str:
        return self["device_id"]

    @property
    def frequency(self) -> str:
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
        cls_str  = f"Model:         {self.model}\n"
        cls_str += f"Band:          {self.band}\n"
        cls_str += f"Channel Name:  {self.channel_name}\n"
        cls_str += f"Device ID:     {self.device_id}\n"
        cls_str += f"Frequency:     {self.frequency}\n"

        cls_str += f"Tags:          {self.tags}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)


class Backup(dict):

    ##################
    ## CONSTRUCTORS ##
    ##################
    def __init__(self,
            type            : str,
            band            : str,
            frequency       : str,
        ) -> None:
        """
        Form a WWB Channel Object from a list of identifiers
        """

        # Set the internal variables, as this is a dict
        self["type"]            : str       = type
        self["band"]            : str       = band
        self["frequency"]       : str       = frequency

        pass

    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ):
        """
        Form a WWB Backup Channel Object from a csv row on the following format:

        `Type,Band,,,,Frequency,,,`
        """
        fields  = csv_line.split(",")

        # The csv string is as follows
        # Model, Band, Channel Name, Device ID, Channel/Group, Frequency, [Tags]*,,
        type            : str   = fields.pop(0)     # Type field
        band            : str   = fields.pop(0)     # Band field
        _                       = fields.pop(0)     # Unused, Channel name field
        _                       = fields.pop(0)     # Unused, Device ID field
        _                       = fields.pop(0)     # Unused, Channel/Group field
        frequency       : str   = fields.pop(0)     # Frequency field
        # The rest is unused

        return cls(type, band, frequency)


    ################
    ## PROPERTIES ##
    ################
    @property
    def type(self) -> str:
        return self["model"]

    @property
    def band(self) -> str:
        return self["band"]

    @property
    def frequency(self) -> str:
        return self["frequency"]
    

    ######################
    ## INTERNAL METHODS ##
    ########################
    def __repr__(self) -> str:
        return super().__repr__()    

    def __str__(self) -> str:
        cls_str  = f"Type:          {self.type}\n"
        cls_str += f"Band:          {self.band}\n"
        cls_str += f"Frequency:     {self.frequency}\n"

        return cls_str

    ###################
    ## OTHER METHODS ##
    ###################
    def to_json(self, indent: int = None):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=indent)