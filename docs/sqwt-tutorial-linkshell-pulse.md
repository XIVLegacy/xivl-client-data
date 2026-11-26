# Tutorial lesson 15 icon pulse declarations

The supplied `TutorialWidgetK15` and `TutorialWidgetP15` forms declare a
second copy of one icon inside a Label. A template for that Label declares a
looping scale and fade on a start command, and a local Window style requests
the start and stop commands from the window lifecycle events.

## Inputs

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. Paths are relative to `client/sqwt/widget/`.
Neither encrypted inputs nor decoded XML are distributed here.

| File | Input bytes | Input SHA-256 | Decoded bytes | Decoded SHA-256 |
| --- | ---: | --- | ---: | --- |
| `TutorialWidgetK15.form` | 4018 | `d2afa6c7de7b8280f34b35eb420ad2c7f353d4869febf01641290c7a253bfb70` | 4010 | `a56384b3eb77ba2ce096c44f9697fb268b1de8f40a793b1d81ef4ad1c6db891b` |
| `TutorialWidgetP15.form` | 4018 | `1cda55fc603c8809a83e30898ac87d50192363675c2d950bd69a2a32a20f6ef8` | 4010 | `f26250ad60cb201ea4cca1138360925c8cf13501926f30d870c09e9ff8238009` |
| `TutorialWidgetK15.tpl` | 2692 | `8b2bd087129c4ecd522720ce052be350bc0426481b4c91a643d978d7bf06372b` | 2684 | `56bd5202e42804597807d30080f01170e81bbaf6c81937afc16327542435b386` |
| `TutorialWidgetP15.tpl` | 2692 | `e002a8e646af47362be6e816bfbabcfe13780256a10248bf0672cef2d3df4e44` | 2684 | `56bd5202e42804597807d30080f01170e81bbaf6c81937afc16327542435b386` |

The two templates decode to the same bytes. The two decoded forms differ only
in the stem inside the root `Name` and inside the second merged dictionary
`Source`. Decode each input with its basename as the key. The `xivl-tools`
command `xivl extract-resource <input> --output <directory> --as sqwt`
reproduces the decoded identities.

## Selection across the lesson forms

All 36 forms `TutorialWidgetK1` to `TutorialWidgetK18` and `TutorialWidgetP1`
to `TutorialWidgetP18` select
`ControlTemplate_Window_TutorialBase` through `Window.Template`. Only K15 and
P15 have a `Window.Style` property element on the root, and only these two
hold a name that contains `NpcLinkshell`. The `Window.Style` element holds one
`StaticResource` with `ResourceKey="Style_Window"`. Each of the two forms
merges `widget/TutorialBase.tpl` and then its own template.

## Form declarations

In both forms a Grid named `Grid` holds two siblings in this order.

| Element | Declarations |
| --- | --- |
| `IconControl` named `IconControl_NpcLinkshell` | `IconDatas="291"`, `Width="24"`, `Height="24"`, `VisualOpacity="0.9"` |
| `Label` named `Label_NpcLinkshell_Anime` | `Template="{StaticResource ControlTemplate_Label_IconAnime}"`, `SqwtStyle="LAB_null"`, `IsHitTestVisible="False"` |

The Label's one child is an `IconControl` named
`IconControl_NpcLinkshell_Anime` with `IconDatas="291"`, `Width="24"` and
`Height="24"`.

## Local Window style

`Style_Window` in the form's own template has `TargetType="{x:Type Window}"`
and an empty `SqwtIsAutoSetSkin` attribute. It has no Setter. Its
`Style.Triggers` holds three `EventTrigger` elements in the order below. Each
holds one `ExecuteCommandAction` whose `CommandTarget` is
`{Binding ElementName=Label_NpcLinkshell_Anime, Mode=OneWay}`.

| `RoutedEvent` | `Command` |
| --- | --- |
| `Shown` | `UILuaCommands.IconAnimeStart` |
| `Closing` | `UILuaCommands.IconAnimeStop` |
| `Hiding` | `UILuaCommands.IconAnimeStop` |

## Label template

`ControlTemplate_Label_IconAnime` in the same file targets `{x:Type Label}`.
It sets `RenderTransform` to `ScaleTransform` and holds a `ContentPresenter`
with `ClipToBounds="False"`. Its triggers are two `CommandTrigger` elements.

The `UILuaCommands.IconAnimeStart` trigger begins a storyboard named
`IconLoopAnime` with `RepeatBehavior="Forever"`. It holds a discrete
`RenderTransformOrigin` key frame of `0.5,0.5` and three `DoubleAnimation`
elements. Each has `Duration="0:0:0.4"`, `ToAccelType="SlowDown"` and
`ToAccelValue="0.8"`.

| Target property | From | To |
| --- | ---: | ---: |
| `RenderTransform.ScaleX` | 1 | 1.4 |
| `RenderTransform.ScaleY` | 1 | 1.4 |
| `VisualOpacity` | 1 | 0 |

The `UILuaCommands.IconAnimeStop` trigger stops `IconLoopAnime` and begins an
unnamed storyboard. That storyboard repeats the origin key frame and animates
`VisualOpacity` to 0 with `Duration="0:0:0"`.

## Limits

The declarations do not establish template or style application, delivery of a
lifecycle event or command, the clock of a storyboard, or a drawn pulse.
`xivl-decomp:docs/resource/sqwt-window-trigger-order.md` documents the native
trigger collection passes.
