# Test Show
---

> Created on: 06 Nov 2022 at 17:47:00

> Created on version: 6.15.0.119

## Show Information

|                            | 0                  |
|:---------------------------|:-------------------|
| Venue                      | Studentersamfundet |
| Address                    |                    |
| Trondheim;Trondheim   7030 |                    |
| Norge                      |                    |
| Phone                      | 12345              |
| Fax                        | 67890              |
| E-mail                     | samf@safsm.d       |
| Notes                      | Test               |


## Customer Information

|                  | 0                |
|:-----------------|:-----------------|
| Point of Contact | Øyvind           |
| Phone            | 1234             |
| Fax              | 90               |
| E-mail           | email1@email.com |

## Inventory Report
    
### RF Zone: Default

#### Active channels (4)

##### No Inclusion Group

| Model   | Band   | Channel Name   | Device ID   | Frequency   | Tags   |
|:--------|:-------|:---------------|:------------|:------------|:-------|
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 540.700 MHz |        |
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 555.450 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 575.200 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 589.000 MHz |        |

#### Backup channels (2)

##### No Inclusion Group

| Type        | Band   | Frequency   |
|:------------|:-------|:------------|
| AD/Standard | G56    | 615.100 MHz |
| PSM1000     | J8E    | 574.450 MHz |

### RF Zone: Test 1

#### Active channels (6)

##### Group 1

| Model   | Band   | Channel Name   | Device ID   | Frequency   | Tags   |
|:--------|:-------|:---------------|:------------|:------------|:-------|
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 521.200 MHz |        |
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 552.075 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 558.200 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 559.225 MHz |        |

##### Group 2

| Model   | Band   | Channel Name   | Device ID   | Frequency   | Tags   |
|:--------|:-------|:---------------|:------------|:------------|:-------|
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 587.725 MHz |        |
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 594.125 MHz |        |

#### Backup channels (3)

##### Group 1

| Type        | Band   | Frequency   |
|:------------|:-------|:------------|
| AD/Standard | G56    | 581.525 MHz |
| PSM1000     | J8E    | 580.400 MHz |

##### Group 2

| Type        | Band   | Frequency   |
|:------------|:-------|:------------|
| AD/Standard | G56    | 579.700 MHz |

### RF Zone: Test 2

#### Active channels (4)

##### Group 2

| Model   | Band   | Channel Name   | Device ID   | Frequency   | Tags   |
|:--------|:-------|:---------------|:------------|:------------|:-------|
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 580.000 MHz |        |
| AD4D-A  | G56    | Shure          | [AD4D-A]    | 584.225 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 577.750 MHz |        |
| PSM1000 | J8E    | Shure          | [P10T]      | 578.225 MHz |        |

#### Backup channels (2)

##### Group 2

| Type        | Band   | Frequency   |
|:------------|:-------|:------------|
| AD/Standard | G56    | 632.650 MHz |
| PSM1000     | J8E    | 596.450 MHz |

## Frequency Coordination Parameters

### Inclusions 

#### User group - Custom

| User Group   | Type   | Frequency                 | TV   |
|:-------------|:-------|:--------------------------|:-----|
| Test         | Range  | 470.000 MHz - 580.000 MHz |      |

#### Inclusion list - Inclusion 1

| Inclusion Group   | Type   | Frequency                 | TV   |
|:------------------|:-------|:--------------------------|:-----|
| Group 1           | Range  | 494.000 MHz - 566.000 MHz |      |
|                   | Range  | 554.000 MHz - 590.000 MHz |      |
| Group 2           | Range  | 566.000 MHz - 636.000 MHz |      |
|                   | Range  | 590.000 MHz - 622.000 MHz |      |

### Exclusions 

#### Active tv (72)

| Type          | Channels                                                                                                                |
|:--------------|:------------------------------------------------------------------------------------------------------------------------|
| Digital Audio | 10A;10B;10C;10D;10N;11A;11B;11C;11D;11N;12A;12B;12C;12D;12N;5A;5B;5C;5D;6A;6B;6C;6D;7A;7B;7C;7D;8A;8B;8C;8D;9A;9B;9C;9D |
| Other         | 10;11;12;2;21;22;23;25;26;28;3;30;33;37;38;4;40;44;45;46;47;48;49;5;50;51;52;53;57;58;59;6;60;61;7;8;9                  |

#### Other exlusions (3)

| Type   | Source   | Frequency                 | Notes   |
|:-------|:---------|:--------------------------|:--------|
| Single | Manual   | 543.350 MHz               |         |
| Range  | Manual   | 734.000 MHz - 738.000 MHz |         |
| Range  | Manual   | 753.000 MHz - 758.000 MHz |         |

