# EXP popup form declarations

The installed FINAL FANTASY XIV 1.23b client declares the experience popup as
one window form and one window template. This page records their text roles
and the storyboard that the popup command starts.

## Source identities and decoding

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. Paths are relative to `client/sqwt/system/ingame/`.
Neither encrypted inputs nor decoded XML are distributed here.

| File | Input bytes | Input SHA-256 | Decoded XML bytes | Decoded XML SHA-256 |
| --- | ---: | --- | ---: | --- |
| `EXPPopupWidget.form` | 1343 | `0e027a2a29f5eafd5ade05003ef6c87a5f372d4e443b95b0eaf5737b88ce5478` | 1335 | `9fa3fe19f50c8a14eb6f8e077c0794f854d53fad510058631a678f09557ab353` |
| `EXPPopupWidget.tpl` | 1789 | `f13d0a891a794b9c3aed3082c521a0d14f1547aeae06d71de01ffb6097d77a50` | 1781 | `a87318086298a419d4f7a0df430ae52d0f7bf92381d4de770145613d7e475c16` |

Both inputs carry the complete SQEX signature `5351455800000000`. Decode with
the basename, including case and suffix, as the ASCII Blowfish key, following
the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). The decoder
uses little-endian block halves and preserves a partial tail. Parse the
decoded text as UTF-8 XML with the standard library ElementTree.

## Form

The root is a `Window` named `Window_EXPPopupWidget`. It sets
`FontEdge="True"`, `IsHitTestVisible="False"`, `Focusable="False"`,
`ClipToBounds="False"`, `DragMode="NoDrag"` and center horizontal and
vertical alignment. Its `SqwtStyleFile` is `common/default.style` and its
`SqwtStyle` is `NULL`. It carries `StringData.Value0="EID_BODY_DYN"`. It
merges `system/ingame/EXPPopupWidget.tpl` and selects the template key
`ControlTemplate_Window_EXPPopup`.

The content is one horizontal `StackPanel` with two `TextBlock` elements:

| Name | Declaration |
| --- | --- |
| `TextBlock_EXPText` | `FontSize="42"`, `FontStyle="Italic"`, `FontType="4"`, bottom aligned, no `Text` |
| `TextBlock_Text` | `Text="@1044/i0"`, `FontSize="20"`, `FontStyle="Italic"`, `Margin="0,0,0,-1"`, bottom aligned |

Both use `SqwtStyle="TBL_null"`. The number text is not declared here. The
native raise path that sets `TextBlock_EXPText` is in
`xivl-decomp:docs/script/exp-popup-raise.md`.

## Template and storyboard

`ControlTemplate_Window_EXPPopup` targets `Window`, holds a
`ContentPresenter` with `ClipToBounds="False"` and sets `RenderTransform` to
`ScaleTransform`. It has one `CommandTrigger` for `EXPPopupAnime.Start` with
one `BeginStoryboard`. Every track targets the window:

| Target property | From | To | Duration | BeginTime |
| --- | ---: | ---: | ---: | ---: |
| `RenderTransformOrigin` | | `0.5,0.5` | discrete key frame at 0 | |
| `VisualOpacity` | 0 | 0 | 0 | |
| `VisualOpacity` | 0 | 1 | 0.3 s | 0 |
| `RenderTransform.ScaleX` | 1.5 | 0.8 | 0.15 s | 0 |
| `RenderTransform.ScaleY` | 1.5 | 0.8 | 0.15 s | 0 |
| `RenderTransform.ScaleX` | 0.8 | 1 | 0.15 s | 0.15 s |
| `RenderTransform.ScaleY` | 0.8 | 1 | 0.15 s | 0.15 s |
| `VisualOpacity` | 1 | 0 | 0.2 s | 2.8 s |

These are static declarations. They do not establish when the command is
raised, the clock that drives the tracks, or the number shown.

The text key `@1044` selects slot 1044 of the English backing block 0
(resource `0x0B4502B5` with row offsets `0x0B4502B7`) described in
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, UISTR-01. The
row decodes to the three-letter text `EXP`. The step assumes the block
starts at key 0, as that page records.
