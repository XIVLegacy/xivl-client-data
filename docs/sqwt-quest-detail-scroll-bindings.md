# QuestDetailWidget scroll input bindings

`widget/QuestDetailWidget.form` declares the scroll area of the quest text and
the key and pad bindings that scroll it. This page records the declarations
only.

## Source identity and reproduction

This is a `client_extraction` finding from the supplied retail 1.23b install,
build `2012.09.19.0001`. The file is 17212 bytes with SHA-256
`27517dfe9c2577efdb28c037a235c1fdb2bf559346ee29eecc2e4864dfc8d04d`. Its
decoded UTF-8 XML is 17204 bytes with SHA-256
`0a7203b9f1948ab117f8b3c13f6c143acc712978cdbda30b77ff16cdb11c9a00`. Decode
it with the basename as the ASCII Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe), parse it
with ElementTree and match tags by local name.

## Scroll area

`ScrollViewer_ExplanationArea` is a `ScrollViewer` in `Grid.Row` 2 with
`SqwtStyle="ScrollViewer_basis"`, `VerticalScrollBarVisibility="Auto"`,
`MaxHeight="508"`, `Margin="2,0,2,0"` and `IsHitTestVisible="False"`.

## Footer grids

Two `Grid` elements share `Grid.Row` 4 and `Margin="0,0,0,2"`.
`Grid_Bottom_Progress` has `Visibility="Collapsed"` and `Grid_Bottom_Order`
has `Visibility="Visible"`. Each holds one `Grid.InputBindings` with the same
eight bindings. Every binding has `IsRepeat="True"` and
`CommandTarget="{Binding ElementName=ScrollViewer_ExplanationArea}"`:

| Command | `KeyBinding` Key | `PadBinding` PadAction |
| --- | --- | --- |
| `ScrollViewer.PageUpCommand` | `PageUp` | `LUp+RLeft` |
| `ScrollViewer.PageDownCommand` | `PageDown` | `LDown+RLeft` |
| `ScrollViewer.LineUpCommand` | `Up` | `LUp` |
| `ScrollViewer.LineDownCommand` | `Down` | `LDown` |

## Boundary

The bindings sit on the footer grids, not on the scroll viewer. The markup
does not show whether a focused footer `Button` takes `Up` and `Down` before
the grid binding sees them. That depends on native focus traversal and
input routing, which this page does not establish.
