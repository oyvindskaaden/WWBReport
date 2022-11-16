import pandas as pd
from datetime import datetime


def to_markdown(wwb_tree: dict) -> str:

    markdown_output = f"""# {wwb_tree["show_name"]}
---

> Created on: {datetime.fromisoformat(wwb_tree["created"]).strftime("%d %b %Y at %H:%M:%S")}

> Created on version: {wwb_tree["wwb_version"]}
"""

    if (wwb_tree["info"]):
        for info in wwb_tree["info"]:
            markdown_output += f"""
## {info.capitalize()} Information

{pd.DataFrame().from_records([wwb_tree["info"][info]]).T.to_markdown()}

# """

    markdown_output += f"""## {wwb_tree["type"]}
    """
# RF Zones
    for zone in wwb_tree["zones"]:
        markdown_output += f"""
### RF Zone: {zone}
"""
        for type in wwb_tree["zones"][zone]:
            markdown_output += f"""
#### {type.capitalize()} channels ({str(wwb_tree["zones"][zone][type]["no_" + type])})
"""

            for group in wwb_tree["zones"][zone][type]:
                if group in "header" or group.startswith("no_"):
                    continue
                markdown_output += f"""
##### {group}

{pd.DataFrame(wwb_tree["zones"][zone][type][group]).to_markdown(index=False)}
"""

# Frequency Coordination Parameters
    markdown_output += """
## Frequency Coordination Parameters
"""
    for param in wwb_tree["parameters"]:
        markdown_output += f"""
### {param.capitalize()} 
"""

        for list in wwb_tree["parameters"][param]:
            if list.endswith("_name") or list.startswith("no_"):
                continue

            markdown_output += f"""
#### {list.replace("_", " ").capitalize()}"""

            if (param == "inclusions"):
                markdown_output += " - " + wwb_tree["parameters"][param][list + "_name"]
            elif (param == "exclusions"):
                markdown_output += f""" ({wwb_tree["parameters"][param]["no_" + list]})"""
            markdown_output += f"""\n
{pd.DataFrame(wwb_tree["parameters"][param][list]).to_markdown(index=False)}
"""

    return markdown_output