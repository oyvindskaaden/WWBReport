# Description of WWB report files

What is not catched by the following regex is CSV.
```(.*,)```

## Show name (Title)

```""\n"(.+)"\s+""``` 
- group1 = Showname
- Contact info comes right after this as proper CSV, without header

## Type of report

```"(.* Report)"\s+``` 
- group1 = Type of report
- New State to read the report that start next line

## RF Zone

```"RF Zone: (.+)"\s+```
- group1 = Name of RF Zone
- Every group have an RF Zone, "Default" is default
- Set RF zone to active group, not seperate state

### Active Channels

```"Active Channels \((\d+)\)"\s+```
- group1 = Amount of active channels in RF Zone
- Equals the number of lines in the following CSV + 2 lines for header and inclusion group.
- Let Pandas or other CSV parser handle this

### Backup Frequenzy

```Backup Frequencies \((\d+)\),(?:Frequency List Source: (.+))?,\s+```
- group1 = Amount of backup frequencies
- group2 = Optional backup frequency source
- Followed by a correct CSV of the backup frequencies

### Inclusion groups in channel lists

```\n(.+) \((\d+)\),{8}```
- group1 = Inclusion group name
- group2 = Number of freq in group

## Frequency coordination parameters

```""\n"Frequency Coordination Parameters"\s```
- Parameters used
- The following parts is in the following order allways
    1. Inclusions
    2. Exclusions
    3. Other Exlusions

### Inclusions

```"Inclusions"\s+```
- Followed by the inclusions

#### User grups

```"User Group List: (.+)"\s+```
- group1 = Name of user group
- This is followed by a proper CSV containing the user groups

#### Inclusion lists

```"Inclusion List: (.+)"\s+```
- group1 = Name of inclusion group
- This is followed by a proper CSV containing all the inclusions.
- Inclusion group is equal to the last defined group in that column.

### Exclusions

```"Exclusions"\s+```

Exclusions are either TV channels or other exclusions (self added)

#### TV Channels

```"Active TV Channels \((\d+)\)"\s+```
- group1 = Amount of excluded TV channels
- Followed by a CSV, but the TV channels are seperated by ", " (comma-space). CSV are not with space.

#### Other Exclusions

```"Other Exclusions \((\d+)\)"\s+```
- group1 = Amount of other exclusions
- Followed by a CSV


## Other 

### Date of creation

```"Created on (.+ at .+)"\s+```
- group1 = Date and time of generation
- Datetime will be in the format ```"%d %b %Y at %I:%M%p"```

### Version of WWB

```"Generated using Wireless Workbench (.+)"\s+```
- group1 = Version of WWB


