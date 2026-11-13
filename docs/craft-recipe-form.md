# Craft recipe form declarations

[Documentation index](README.md)

The HD `widget/CraftRecipeWidget.form` declares a Window named
`Window_CraftRecipeWidget` with the common Window template. Its merged
resource dictionaries are `common/WINBasis.tpl` followed by
`widget/CraftRecipeWidget.tpl`.

## Material list

Within `Grid_MaterialName`, the unnamed Label at decoded line 263 uses
`LAB_basis_ContentWindow`. It declares `Focusable="False"`,
`IsHitTestVisible="False"` and `KeyboardNavigation.IsTabStop="False"`.
Its only direct child is the ListBox named `ListBox_Material` at line 264.

The ListBox declares both `IsTabStop="False"` and
`KeyboardNavigation.IsTabStop="False"`, with `Focusable="False"` and
`IsHitTestVisible="False"`. Its eight direct ListBoxItems are named
`Item_1` through `Item_8`. Each selects `ControlTemplate_Material` from
the form's widget dictionary.

## Operation button

In `Grid_Button`, the childless Button named `Button_Operate` at
decoded line 410 declares `UILuaCommands.Operate`, `@3090` content,
`BTN_basis` and minimum width 100. Its declaration supplies no
`CommandTarget`, `CommandParameter` or `ClickMode`.

These declarations identify static controls and template selections.
Runtime material values, focus dispatch and recipe acceptance require
their respective script, native or session evidence.

## Source and reproduction

The inputs are under `client/sqwt/widget/` in client build
`2012.09.19.0001`. Decode strict UTF-8 using the basename as the
key with the [SQEX format](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/sqex.md).
Re-encrypting each decoded body and prepending the original signature
reproduces the matching container.

| File | Container bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `CraftRecipeWidget.form` | 40239, `8ae6c349c587a8798b637e1926c940ab1ebc379eddc7a72062ac6bcb647b682a` | 40231, `57314bc550b3963cd5e7fe29457b71dd9387c33c9d56a57a4c31a0c26b69af5c` |
| `CraftRecipeWidget.tpl` | 7290, `6c52e66d5554af1f9b35075724880ba667293684cf7374ebc457c0bda1fe76ef` | 7282, `f51c3e4abe57199082bc7579a0864a2ae09e01ab203a69720fde1a80af13ecbc` |
