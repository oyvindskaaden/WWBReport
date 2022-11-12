import json

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
        type            = fields.pop(0)     # Type field
        band            = fields.pop(0)     # Band field
        _               = fields.pop(0)     # Unused, Channel name field
        _               = fields.pop(0)     # Unused, Device ID field
        _               = fields.pop(0)     # Unused, Channel/Group field
        frequency       = fields.pop(0)     # Frequency field
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