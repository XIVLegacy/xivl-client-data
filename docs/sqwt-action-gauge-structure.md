# ActionGauge cast progress declarations

This finding records static client extraction from an owner-supplied 1.23b install. The files do not independently establish the executable build identity. Identified input files and decoded documents are restricted inputs and are not distributed here.

## Source identity and reproduction

Paths below are relative to `client/sqwt/`. Widget files are under `widget/`, and the style and skin files are under `common/`.

| Basename | Input bytes | Input SHA-256 | Decoded bytes | Decoded SHA-256 |
| --- | ---: | --- | ---: | --- |
| `ActionGaugeWidget.form` | 2298 | `74e3dd1d832a37a8301d2a8c1af84717bc46b7083bdaa2cc69a421d991c319ca` | 2290 | `632d006a0f5f082d8d2249ad59f64a0763500e9baf573faff399023ee6748a14` |
| `ActionGaugeWidget.tpl` | 4291 | `7e103f7db486ce3da5bb37f4e7f49468aacdb9701129f60eee393d8b7185e98c` | 4283 | `5efd76d75393d4d0357227d43388bbfad4ba9098dfcf674f314063bcee47856c` |
| `ActionGaugeWidget.sd.form` | 3487 | `83d47495ac4146ebc926b3c268b506bcc692c130b9f0a47f522ed75128924554` | 3479 | `346c956f181b8cb0895591618ff9fb9bd921de793197a0808fc86c340dcf1104` |
| `ActionGaugeWidget.sd.tpl` | 6020 | `856e3c35846a7181f52ad60262dc5050775f024b63d06d5ed415e0245203fb28` | 6012 | `b3cad49969627478f8aa47ed98955afeb1c9d8174a395c76a250a9cd745abda8` |
| `default.style` | 353783 | `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` | 353775 | `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |
| `default.skin` | 141967 | `6788f2986d9cc8aeab83fcdbcf7a9115d3576ecfabf40529cc861f41f0df5640` | 141959 | `929e65e9d5f191292d9b044e3e659ba115f18f6b3d8a82894046a7c75cbcad5a` |

All six containers carry the complete SQEX signature and pass strict UTF-8 decoding, XML parsing and byte-exact re-encryption. Use the basename, including case and suffix, as the Blowfish key. Decrypt after the eight-byte signature with little-endian block halves, retaining a trailing partial block. The recipe is `xivl-tools:docs/formats/sqex.md`, and the decoder is `xivl-tools:tools/blowfish.py`, 4324 bytes, SHA-256 `7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`. Select namespace-qualified elements without evaluating bindings or assuming defaults.

## Progress owner and template role

Both forms contain one `ProgressBar` named `ProgressBar_MagicCast_Main` in namespace `http://namespace.square-enix.com/sqwt`. Its containment chain is `Window/Window_ActionGaugeWidget -> Grid/unnamed -> StackPanel/unnamed -> Grid/Grid_MainCommand -> ProgressBar/ProgressBar_MagicCast_Main`. It has no authored children.

The owner selects `ControlTemplate_ProgressBar_CastGauge` from its corresponding widget template. That template declares a separate `ProgressBar` named `ProgressBar_CastGauge`. This is a template role, rather than a child declared under the form owner. Both owners declare empty `Value`, no `Maximum` or `Minimum`, and no `Visibility` or `VisualOpacity`. The inner part also declares empty `Value`, no `Minimum`, `Visibility` or `VisualOpacity`, and binds its `Maximum` to the templated parent Maximum in OneWay mode. These absences establish no native defaults.

The owner selects style `PRB_magicCastH`. The HD owner has margin `27,0,0,0` and minimum width `206`. The SD owner has margin `23,0,0,0` and minimum width `166`. The HD form imports `widget/ActionGaugeWidget.tpl`, and the SD form imports `widget/ActionGaugeWidget.sd.tpl`. Neither imports the common WINBasis templates.

The selected cast template has these command declarations:

| Command | Declared action |
| --- | --- |
| `UILuaCommands.StartCastGauge` | Begin `StartCastGauge`, targeting inner `ProgressBar_CastGauge.Value` |
| `UILuaCommands.PauseCastGauge` | Pause `StartCastGauge` |
| `UILuaCommands.RestartCastGauge` | Resume `StartCastGauge` |

The start trigger binds its source name to the templated parent Name. Its animation binds From to parent Value, To to parent Maximum and Velocity to parent FloatData.Value0, all in OneWay mode. It declares no Duration. The declarations establish no command delivery or animation execution.

## Selected style and skin references

`common/default.style` and `common/default.skin` use unqualified element names. The style root selects `common/default.skin`. Under `Widget Type=ProgressBar`, `PRB_magicCastH` names `HorizontalBackground` and `HorizontalIndicator` parts. Both reference Window styles. The background selects `PRB_magicCast_bgH`, and the indicator selects `PRB_magicCast_indicatorH`. Their Window styles select the corresponding named skin for Normal, Hover, Active, Disabled and Focused conditions. Anchored, Reserved and Droppable conditions use literal `NULL`. The skin has no named `NULL` declaration. Its native meaning remains unresolved.

The background skin is a three-cell row with HitMargin `1,0,1,0` and SkinBorderThickness `9,0,9,0`. The indicator is a merged skin with HitMargin `0,0,3,0`. Its references, in order, are the indicator background with IsMinimumSize false and the indicator frame with no IsMinimumSize attribute. The referenced cell skins declare:

| Skin | Cells | Additional attributes | Rectangle declarations in order |
| --- | --- | --- | --- |
| `PRB_magicCast_bgH` | `3,1` | As above | `738,839,12,32`, `750,839,2,32`, `752,839,12,32` |
| `PRB_magicCast_indicator_bgH` | `3,1` | SkinMargin `0,0,4,0` | `1015,24,3,32`, `1018,24,1,32`, `1019,24,3,32` |
| `PRB_magicCast_indicator_frameH` | `3,1` | HitMargin `5,0,3,0` | `372,617,1,32`, `373,617,1,32`, `374,617,8,32` |

All nine cells declare Stretch draw mode. Their containing CellSkins selects literal `common/default.dds`. An authenticated candidate `common/default.win32.gtex` is 4194336 bytes with SHA-256 `c7f11f369e21b19b79fbe174bb10f78f7312b366383db9774e873238b2d5d88f` and GTEX magic. These declarations and identities do not prove a native alias from the literal DDS name to this candidate. No atlas pixels were decoded or rendered for this finding.

The template inner part has no style attribute. Propagation of the outer style into that part, cell placement, clipping, skin state selection and resource lookup require a separate native contract.

## Scope of isolation

The main command grid also contains the command icon and text. In HD the icon is under a sibling Border, and in SD it is a direct sibling. Neither icon nor text is a descendant of the progress owner. The SD form also declares a separate collapsed sub-command grid and additional action gauge controls. A static selection of the main progress owner, its cast template role and the selected style and skin declarations excludes those siblings.

The Window template separately declares Shown, Closing and Hiding animations of VisualOpacity and SqwtTopOffset. Closing completes DestroyWindow and Hiding completes InvisibleWindow. These window declarations do not establish a progress-only opacity animation. No native event delivery, display frame, rendered appearance or live-client result is established here.
