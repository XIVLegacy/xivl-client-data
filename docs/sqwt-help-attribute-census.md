# Help attribute census

This page counts the `Help.Type` and `Help.Value0` attributes over the whole
`client/sqwt` markup set. It records which declarations take a literal text
reference and which take a binding.

## Input and method

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The set is every `.form`, `.tpl` and `.style` file
under `client/sqwt`, 1122 files in all. Decode each with the basename as the
ASCII Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). Parse the
decoded text with the standard library ElementTree, match attribute names by
local name and select every element that carries `Help.Type` or
`Help.Value0`. One file, `system/common/Staffroll.form`, does not parse
because of an unbound namespace prefix and is outside the counts. A literal
text reference is `@` followed by decimal digits.

## Counts

No selected file declares a `Setter` for either attribute, and no decoded text
names `Help.Value1` or a higher index. The 871 selected elements divide as
follows:

| `Help.Type` | `Help.Value0` | Elements |
| --- | --- | ---: |
| `1` | Literal text reference | 836 |
| `0` | Literal text reference | 11 |
| `0` | Absent | 2 |
| `1` | Binding | 9 |
| `1` | Absent | 5 |
| Binding | Binding | 5 |
| Absent | Literal text reference | 3 |

No element declares the literal `Help.Type="2"`.

## Bound values

All bindings are `OneWay` XPath bindings. These elements declare
`Help.Type="1"` with a bound `Help.Value0`:

| File under `widget/` | Element and `Name` | XPath | Elements |
| --- | --- | --- | ---: |
| `AchievementListWidget.tpl` | `Grid`, unnamed | `@hoverHelp` | 1 |
| `JournalListWidget.tpl` | `IconControl_CategoryIcon` | `@CategoryIconHelp` | 1 |
| `LinkshellMembersListWidget.tpl` | `IconControl_Status` | `@StatusIconHelp` | 1 |
| `LinkshellMembersListWidget.tpl` | `IconControl_Reader` | `@RankIconHelp` | 1 |
| `LogColorSettingWidget.tpl` | `Button_Command` | `@Help` | 1 |
| `LogSettingWidget.tpl` | `Grid`, unnamed | `@Help` | 1 |
| `MainMenuWidget.tpl` | `Button_Command` | `@Help` | 3 |

The five elements that bind both attributes are in
`widget/JournalListWidget.tpl`:

| Element and `Name` | `Help.Type` XPath | `Help.Value0` XPath |
| --- | --- | --- |
| `IconControl_Active` | `@HelpTypeIconActive` | `@HelpValue0IconActive` |
| `IconControl_Clear` | `@HelpTypeIconClear` | `@HelpValue0IconClear` |
| `IconControl_Fail` | `@HelpTypeIconFail` | `@HelpValue0IconFail` |
| `Grid`, unnamed | `@ComboBoxItemHelpType` | `@ComboBoxItemHelpValue0` |
| `TextBlock_CategoryTitle` | `@TitleHelpType` | `@TitleHelpValue0` |

These are static declarations. They do not establish the values a bound
element receives at run time. Script writers of the same properties are
outside this census.
