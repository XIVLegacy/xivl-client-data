# Root windows with an empty MinWidth

Five installed forms write `MinWidth=""` on their root `Window`. The markup
declares the attribute with no text. This page lists the files.

## Source identity and reproduction

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. Decode every `.form`, `.tpl` and `.style` file under
`client/sqwt` with the basename as the ASCII Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe), parse it
with ElementTree and select the files whose root local tag is `Window` and
whose `MinWidth` attribute equals the empty string.

| Path under `client/sqwt` | Bytes | SHA-256 of the file |
| --- | ---: | --- |
| `widget/ItemHelpWidget.form` | 45183 | `9108081affa967b9946ebc6ac9d90d0944e3193abc73111b5e8310c377b5fb54` |
| `widget/ItemSalesHistoryWidget.form` | 3096 | `ac6ca715895cef475389579eaec953632d18f1d189258af826e60439560dd257` |
| `widget/ItemSearchListWidget.form` | 3735 | `a5533d3928d006c032198f949de839e7587e81ddd95317428855daecdb55268a` |
| `widget/ItemSelesHistoryWidget.form` | 3168 | `514e5dc9873c03f68d960355be60a4701b0714df224d7d0c1692cace2a8049bd` |
| `widget_c/ItemSearchListWidget.form` | 3641 | `6571254f9fd58a236afb1666ef344c2164e6b6dc9f15a259dfff6fce23e5961e` |

## Boundary

The native reader of a length attribute and its treatment of empty text are
not traced. The markup does not establish a zero floor, an absent attribute
or a parse error.
