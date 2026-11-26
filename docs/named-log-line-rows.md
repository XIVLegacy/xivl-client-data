# Named log line rows

Selected rows of `xtx/_text_ui` that format a log line from a source name and a
text. These are `client_extraction` values from extraction `2012.09.19.0001`,
read from `xtx__text_ui.csv` as `xivl extract` writes it. Its file bytes match
[tables.json](../manifests/tables.json). The definition and its five languages
are on the
[interface string coverage](boot-select-and-error-rows.md#interface-string-key-coverage)
section. No row text beyond the separator is reproduced.

## Row selection

For a numeric `LogFormat` the client takes the text row `LogFormat + category`
and supplies the source name as string argument 1 and the text as string
argument 2, under
`xivl-decomp:docs/resource/logcontrol-line-format.md`, LF-04. The LogWidget
form sets `LogFormat` to 2400, so categories 35, 38, 39 and 40 take rows 2435,
2438, 2439 and 2440. The shipped scripts that pass a named source are counted
in `xivl-client-scripts:docs/named-script-log-lines.md`.

## Layout

Each of the four rows holds, in order, a colour token, an edge colour token,
string argument 1, a separator, string argument 2, a closing edge colour token
and a closing colour token. This holds in all five language columns. The `fr`
column of each row also holds the token `02 1D 01 03` between string argument 1
and the separator.

| Column language | Literal between the two arguments |
|---|---|
| `ja` | space, colon, space |
| `en` | colon, space |
| `de` | colon, space |
| `fr` | the token above, then colon, space |
| `chs` | space, colon, space |

The first token of each row is a colour token whose operand differs by row. The
table gives the whole token. It is the same in the five columns.

| Row | First colour token bytes |
|---:|---|
| 2435 | `02 13 06 FE FF FF FF FF 03` |
| 2438 | `02 13 06 FE FF FF FF FF 03` |
| 2439 | `02 13 06 FE FF FF 8C C6 03` |
| 2440 | `02 13 06 FE 99 CC CC CC 03` |

The rendering of the colour operands and of the `0x1D` token is outside this
page. `xivl-decomp:docs/resource/rich-text-colour-tokens.md` owns the colour
token handlers.

## Reproduction

Extract the install with `xivl extract`, check `xtx__text_ui.csv` against
tables.json, and read the rows with the keys above. The column labelled 0 is
`ja`, and the labels 1 to 4 follow the declaration order `en`, `de`, `fr` and
`chs`.
