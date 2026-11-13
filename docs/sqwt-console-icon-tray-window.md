# Console icon tray window declarations

The HD `ConsoleIconTrayWidget` form selects a shared Window template and a
local Window style. The template declares lifecycle animations on unnamed
recipients. The style names two backdrop Borders and declares a separate
balloon help timer.

## Installed inputs

This `client_extraction` finding covers supplied build `2012.09.19.0001`.
Paths are relative to `client/sqwt/`.

| Path | Container bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `widget/ConsoleIconTrayWidget.form` | 11166, `180b7d709e588ec86fccead327aec813d4baab5b41ead05d2610cf318e787a0d` | 11158, `efbf73d1ac6307ca4983e9eeaf3170ab507d48e012d4c797ae360119d49d5f3e` |
| `widget/ConsoleIconTrayWidget.tpl` | 20238, `f3c362bb64d9e9b07dd60b2ba95e1b868640e43c82558b83c24d1fd32d3378f1` | 20230, `9f1f5a2c79c2d8b35ea0d0b510c5536bcb43464da236ce1f9dea665f01937386` |
| `common/WINBasisLight_noGrayout.tpl` | 4303, `be271e92c52765dd1cfd8c786c0f77144440520b84239f08db5b0c21c97c8949` | 4295, `47271a67f14e47e0fb458e1a211de9366b17c112576e951668bd519e116ee6d8` |

Use the [SQEX recipe](sqwt-ask-structure.md#reproduction-recipe) with each
original basename. All three inputs have signature `5351455800000000`.
Strict UTF-8 decoding and namespace-aware parsing succeed. Re-encrypting
each decoded payload and prepending the signature reproduces the input.
Python Expat provides the one-based decoded XML locations below.

## Root selections and targets

`Window_ConsoleIconTrayWidget` declares `common/default.style`, `WIN_null`,
right and bottom content, startup and outer alignments, and `Margin` value
`0,0,20,32` at form line 1. The same element declares `Focusable` and
`IsTabStop` false, `KeyboardNavigation.DirectionalNavigation` `Cycle`, and
literal `StringData.Value0` `10`.

The root merges `common/WINBasisLight_noGrayout.tpl` before
`widget/ConsoleIconTrayWidget.tpl` at lines 5-6. Its `Window.Template`
property element at lines 10-12 selects `ControlTemplate_Window_WINBasisLight`
from the common dictionary. Its following `Window.Style` at lines 13-15
selects `Style_Window` from the local dictionary. Each selector contains
one `StaticResource` with only its literal `ResourceKey`.

The root's unnamed Grid begins at line 16. Its first two children, at
lines 17-18, are `Border_Background` and `Border_Background_2`. Each is a
childless Border with literal `SqwtStyle` `BOD_basis_npcLinesBody`,
`IsHitTestVisible` `False` and `VisualOpacity` `0`. Each name is unique in
the form. The selected common template declares neither name.

## Selected template and style

The selected `ControlTemplate` at common template lines 2-73 has target
`{x:Type Window}`. The identical common carrier is described in the
[PlayerParameter Window template declarations](sqwt-player-parameter-structure.md#selected-window-template-declarations).
That section owns its `Grid_Content`, `ContentPresenter`, initial offset
setters, all ten triggers, and lifecycle track operands. The three lifecycle
storyboards have only unnamed track recipients. Their target property names
are `RenderTransformOrigin`, `VisualOpacity`, `SqwtTopOffset` and
`SqwtLeftOffset`.

The local `Style_Window` at lines 236-295 has target `{x:Type Window}` and
an empty `SqwtIsAutoSetSkin` attribute. It has one `Style.Triggers` child
and no direct Setter. Its first four triggers are `MultiTrigger` elements.
Each begins with one `MultiTrigger.Conditions` containing `IsMouseOver` then
`IsAnchorWithin`. Each condition declares only its `Property` and `Value`.
The two animation targets, in order, are `Border_Background` and
`Border_Background_2`.

| Trigger line | `IsMouseOver` | `IsAnchorWithin` | Ordered actions | `VisualOpacity` To values |
| --- | --- | --- | --- | --- |
| 238 | `True` | `True` | Unnamed Begin at 243, Stop `Fadeout` at 249 | `1`, `0.5` |
| 251 | `False` | `True` | Unnamed Begin at 256, Stop `Fadeout` at 262 | `1`, `0.5` |
| 264 | `True` | `False` | Unnamed Begin at 269, Stop `Fadeout` at 275 | `1`, `0.5` |
| 277 | `False` | `False` | Begin named `Fadeout` at 282 | `0`, `0` |

Each Begin contains one Storyboard with no attributes and two childless
`DoubleAnimation` elements. Each animation declares only `To`,
`Duration="0:0:0.2"`, `Storyboard.TargetName`, and
`Storyboard.TargetProperty="VisualOpacity"`. The Stops name the fourth
Begin using only `BeginStoryboardName`. The MultiTrigger and condition
wrapper elements have no attributes.

The fifth and final trigger is `UIFormCommands.TimerStart` at line 289.
Its unnamed Begin at line 290 contains one empty Storyboard. The two
Storyboard attributes are `CompletedCommand="UIFormCommands.TimerFinish"`
and `BeginTime` with a OneWay `ElementName` binding to
`Window_ConsoleIconTrayWidget`, path `StringData.Value0`. This is the only
binding in the selected Style. Its source name equals the raw form root name.

The Style's animation tracks declare explicit backdrop targets, while the
shared template's tracks omit a target. The markup alone leaves the native
recipient of an unnamed track, first condition evaluation, pointer and anchor
notifications, and timer completion delivery unresolved. The native collection
passes and separate timer consumer are documented in
`xivl-decomp:docs/resource/sqwt-window-trigger-order.md`, "Conditional event
passes", and `xivl-decomp:docs/net/confirm-offer-timeout-evidence.md`, "Timer
consumers and limits".
