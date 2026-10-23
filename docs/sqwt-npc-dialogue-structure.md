# NPC dialogue form and template declarations

## Source and extraction

This finding records static client-asset extraction metadata
(`client_extraction`) for declared build `2012.09.19.0001`. It covers only
`client/sqwt/widget/NpcSayWidget.form` and
`client/sqwt/widget/NpcSayWidget.tpl`. The build is supplied provenance.
The identities and results below identify the supplied inputs, which are
not distributed with this repository. Public metadata alone cannot
independently reproduce the extraction.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Form input | 1848 | `d373fb867d84c5e1137b985f6523d01d67bda0b30d551939152c035190562346` |
| Form decoded strict UTF-8 XML | 1840 | `752613f6479b9271e3634e287b03b06b96f5bce7208ad451731f56eabbf454e2` |
| Template input | 3931 | `fe83c1e6cb8ec220f65f34e9647b42415c9362811a9db5a2bf17fe3408ac24e3` |
| Template decoded strict UTF-8 XML | 3923 | `5abae4a6742c78e84fa4d9b9822c82ae7ea5ec442e04578d8067610fd7d8676b` |

Both inputs carry the exact eight-byte signature `5351455800000000`.
The supplied extraction reports strict UTF-8 decoding, XML parsing and
byte-exact re-encryption for both inputs.

## Reproduction recipe

Use the basename-key SQEX format described in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/docs/formats/sqex.md#L17-L42).
Use the existing
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/tools/blowfish.py#L60-L125),
4324 bytes, SHA-256
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`.

1. Require each input's byte size, SHA-256 and complete signature above.
2. Initialize `Blowfish` separately with the ASCII basename including its
   suffix: `b"NpcSayWidget.form"` or `b"NpcSayWidget.tpl"`.
   Decrypt the bytes after the signature. The decoder uses little-endian
   block halves and preserves a final partial block.
3. Require each decoded byte size and SHA-256 above. Decode with strict
   UTF-8 and parse with Python's standard-library `xml.etree.ElementTree`.
4. Re-encrypt the decoded bytes, prepend the original signature and require
   byte-for-byte equality with the input.
5. Select the namespace-qualified elements and exact attribute values below.
   Preserve raw strings without resolving references or applying defaults.

## Form and template identity

The element namespace is `http://namespace.square-enix.com/sqwt`.
The form root is `Window`, with raw `Name="Window_NpcSayWidget"`.
The form contains exactly one element for each selected name:

| Element tag | Raw `Name` |
|---|---|
| `Window` | `Window_NpcSayWidget` |
| `TextBlock` | `TextBlock_NpcName` |
| `LogControl` | `LogControl_NpcSay` |

`TextBlock_NpcName` has no `Text` or `Content` attribute and no child
elements. This is an absence observation on this selected node only.
The names identify the selected speaker and body controls for this finding.
Their runtime text assignment is unresolved.

The form's `ResourceDictionary/@Source` is `widget/NpcSayWidget.tpl`.
Its `Window.Template/StaticResource/@ResourceKey` is
`ControlTemplate_Window_NpcSay`. The identified template has root
`ResourceDictionary` and exactly one `ControlTemplate`. That element has
raw `TargetType="{x:Type Window}"` and `x:Key="ControlTemplate_Window_NpcSay"`,
where `x` denotes `http://namespace.square-enix.com/sqwt/x`.
The two key strings match exactly. This establishes string equality,
without establishing resource loading or resolution.

## Selected trigger declarations

The following declarations are inside `ControlTemplate.Triggers` in the
identified template. Stop names are raw `StopStoryboard/@BeginStoryboardName`
values, listed in document order. Begin names are raw
`BeginStoryboard/@Name` values.

| Selector | Stop names | Begin name | Nested `Storyboard/@CompletedCommand` |
|---|---|---|---|
| `CommandTrigger/@Command="UILuaCommands.NpcSayStart"` | `HidingAnimation`, `ClosingAnimation` | `OpeningAnimation` | Absent |
| `CommandTrigger/@Command="UILuaCommands.NpcSayEnd"` | `OpeningAnimation`, `HidingAnimation` | `ClosingAnimation` | Absent |
| `EventTrigger/@RoutedEvent="Closing"`, `@Name="WindowClose"` | `OpeningAnimation`, `HidingAnimation`, `ClosingAnimation` | Absent | `ApplicationCommands.DestroyWindow` |
| `EventTrigger/@RoutedEvent="Hiding"`, `@Name="WindowHide"` | `OpeningAnimation`, `ClosingAnimation` | `HidingAnimation` | `ApplicationCommands.InvisibleWindow` |

Each selected nested storyboard declares a
`PropertyAnimationUsingKeyFrames/@Storyboard.TargetProperty` of
`RenderTransformOrigin`, with a `DiscreteValueKeyFrame/@Value` of `0.5,0.5`.
Each also declares a `DoubleAnimation/@Storyboard.TargetProperty` of
`VisualOpacity`. Its raw `To` is `1` for `NpcSayStart` and `0` for
`NpcSayEnd`, `Closing` and `Hiding`.
These selected animation elements have no `Storyboard.TargetName`
attribute. No implicit target is inferred.

## Claim boundary

These are raw static declarations. They do not establish command delivery,
event order, animation timing or execution, completion behavior, text binding,
player state, rendering, or a runtime reuse contract. No style, font asset,
computed binding or layout was resolved. Dependencies beyond the identified
form and template remain unread, so their transitive closure is unresolved.
No live-client result is claimed. No XML body or client bytes are distributed.
