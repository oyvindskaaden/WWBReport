import json

class Channel(dict):
    model           : str       = ""
    band            : str       = ""
    channel_name    : str       = ""
    device_id       : str       = ""
    frequency       : str       = ""
    tags            : list[str] = []

    def __init__(self, 
            model           : str   = "",
            band            : str   = "",
            channel_name    : str   = "",
            device_id       : str   = "",
            frequency       : str   = "",
            tags            : list  = []
        ) -> None:

        self.model              = model
        self.band               = band
        self.channel_name       = channel_name
        self.device_id          = device_id
        self.frequency          = frequency
        self.tags               = tags

        self["model"]           = model
        self["band"]            = band
        self["channel_name"]    = channel_name
        self["device_id"]       = device_id
        self["frequency"]       = frequency
        self["tags"]            = tags

        pass

    
    # Maybe overload this function?
    @classmethod
    def from_csvrow(
            cls,
            csv_line        : str
        ) -> None:

        fields  = csv_line.split(",")
        print(fields)

        model           = fields.pop(0)     # Model field
        band            = fields.pop(0)     # Band field
        channel_name    = fields.pop(0)     # Channel name field
        device_id       = fields.pop(0)     # Device ID field
        _               = fields.pop(0)     # This field is unused
        frequency       = fields.pop(0)     # Frequency field
        tags            = fields[:-2]       # The rest, but not the last 2, are tags

        return cls(model, band, channel_name, device_id, frequency, tags)

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    

    def __str__(self) -> str:
        cls_str  = f"Model:         {self.model}\n"
        cls_str += f"Band:          {self.band}\n"
        cls_str += f"Channel Name:  {self.channel_name}\n"
        cls_str += f"Device ID:     {self.device_id}\n"
        cls_str += f"Frequency:     {self.frequency}\n"

        cls_str += f"Tags:          {self.tags}\n"

        return cls_str