# Window Hiding trigger census

The installed templates declare how a window animates when it is hidden.
This page counts those declarations over the whole `client/sqwt` markup set
and records the ActionGauge window timelines.

## Input and method

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The set is every `.form`, `.tpl` and `.style` file
under `client/sqwt`, 1122 files in all. Decode each with the basename as the
ASCII Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). Parse the
decoded text with the standard library ElementTree and match tags by local
name. One file, `system/common/Staffroll.form`, does not parse because of an
unbound namespace prefix and is outside the counts.

## Hiding event triggers

An `EventTrigger` whose `RoutedEvent` is `Hiding` occurs in 136 files, once in
each, and every one of the files is a `.tpl`. In 133 files the trigger holds a
`BeginStoryboard` with a `Storyboard` whose `CompletedCommand` is
`ApplicationCommands.InvisibleWindow`. The triggers of the other 3 files hold
no `BeginStoryboard`. In `widget/PopupHelpWidget.tpl` the trigger holds two
`StopStoryboard` elements. In `widget/TutorialWidgetK15.tpl` and
`widget/TutorialWidgetP15.tpl` it holds one `ExecuteCommandAction`
([lesson 15 icon pulse](sqwt-tutorial-linkshell-pulse.md#local-window-style)).

The `VisualOpacity` `DoubleAnimation` of the trigger, counted per file:

| From | To | Duration | BeginTime | Files |
| --- | --- | --- | --- | ---: |
| 1 | 0 | `0:0:0.2` | `0:0:0` | 126 |
| omitted | 0 | `0:0:0.2` | `0:0:0` | 2 |
| 1 | 0 | `0:0:0.3` | `0:0:0.1` | 3 |
| 1 | 0 | `0:0:0.3` | `0:0:0` | 2 |
| none declared | | | | 3 |

The first animation of each file in document order was read. The Hiding
declarations establish no easing choice and no event delivery. They do not
show when the client starts the clock or whether it draws the span.

## ActionGauge window timelines

The `ControlTemplate_Window_ActionGauge` template of `widget/ActionGaugeWidget.tpl`
(decoded SHA-256 `5efd76d75393d4d0357227d43388bbfad4ba9098dfcf674f314063bcee47856c`,
the identity in [ActionGauge cast progress
declarations](sqwt-action-gauge-structure.md#source-identity-and-reproduction))
declares three `EventTrigger` elements. Each `BeginStoryboard` also holds a
`RenderTransformOrigin` key frame of `0.5,0.5`.

| Event | Stops | `VisualOpacity` | `SqwtTopOffset` | Completion |
| --- | --- | --- | --- | --- |
| `Shown` | `ClosingAnimation`, `HidingAnimation` | From 0 to 1 | To 0 | none |
| `Closing` | `OpeningAnimation`, `HidingAnimation` | From 1 to 0 | To 5 | `ApplicationCommands.DestroyWindow` |
| `Hiding` | `OpeningAnimation`, `ClosingAnimation` | From 1 to 0 | To 5 | `ApplicationCommands.InvisibleWindow` |

Every animation has `Duration="0:0:0.2"` and `BeginTime="0:0:0"`. The
`SqwtTopOffset` animations declare no From. The template declares no
`SqwtLeftOffset` animation.
