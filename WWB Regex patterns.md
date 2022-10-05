# Description of WWB report files

## Show name (Title)

```""\n"([\w|\s]*)"\s+""``` 
- group1 = Showname
- Contact info comes right after this as proper CSV

## Type of report

```""\n"([\w\s]* Report)"\s+``` 
- group1 = Type of report
- New State to read the report that start next line

### RF Zone

```"RF Zone: ([\w\s]+)"\s+```
- group1 = Name of RF Zone
- Every group have an RF Zone, "Default" is default
- Set RF zone to active group, not seperate state

### Active Channels

```"Active Channels \((\d+)\)"\s+```
- group1 = Amount of active channels in RF Zone
- Equals the number of lines in the following CSV + 2 lines for header and inclusion group.
- Let Pandas or other CSV parser handle this

### Backup Frequenzy

```Backup Frequencies \((\d+)\),(?:Frequency List Source: ([\w\s]+))?,\s+```


## Frequency coordination parameters

```""\n"Frequency Coordination Parameters"\s```
- Parameters used
- The following parts is in the following order allways
    1. Inclusions
    2. Exclusions
    3. Other Exlusions

### Inclusions

```"User Group List: ([\w\s]+)"\s+```
- group1 = Name of user group
- This is followed by a proper CSV containing the user groups

```"Inclusion List: ([\w\s]+)"\s+```
- group1 = Name of inclusion group
- This is followed by 




