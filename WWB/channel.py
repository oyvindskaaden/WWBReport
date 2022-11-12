import json

class Channel(dict):

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
        model           = fields.pop(0)     # Model field
        band            = fields.pop(0)     # Band field
        channel_name    = fields.pop(0)     # Channel name field
        device_id       = fields.pop(0)     # Device ID field
        _               = fields.pop(0)     # This field is unused, the Channel/Group
        frequency       = fields.pop(0)     # Frequency field
        tags            = fields[:-2]       # The rest, but not the last 2, are tags

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