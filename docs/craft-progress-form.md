# Craft progress form declarations

The installed FFXIV 1.23b HD keyboard form loads a local template for its
progress gauge and declares the craft point, quality point and HQ rate
text roles. The local template also declares a timer-command style with an
explicit sound action volume.

## Installed inputs

The supplied build is `2012.09.19.0001`. Paths are under
`client/sqwt/widget/`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `CraftProgressWidget.form` | 9565 | `ccd83bd31bf0885fa8b480bad84b454624f70598a1e5ad417c812ff56fb8fb42` |
| Decoded form | 9557 | `9db3d980959e3caa259d41270734e59bf5b2cf50abf9d131dd570ef7ba905197` |
| `CraftProgressWidget.tpl` | 4315 | `35820be4f2758f15c388d828d369fd86e668da143d6459724c761733f9fff983` |
| Decoded template | 4307 | `b09866509c602637aa4404ee1e3b994f2f148995601f6544925cf0b8d149282e` |

The [SQEX recipe](sqwt-ask-structure.md#reproduction-recipe) reproduces both
strict UTF-8 documents with the original basename as the key. Re-encrypting
each payload and prepending the original signature reproduces its input.

## Form and timer style

The form's root is `Window_CraftProgressWidget`. Its resource dictionary
sources are `widget/CraftProgressWidget.tpl` and `common/WINBasis.tpl`,
in document order. `ProgressBar_Percentage` declares template
`{StaticResource TemplateControl_ProgressBar}` and style
`PRB_parameter_tpMiddleH`. Its template contains the
`TemplateProgressBar_Percentage` ProgressBar with `Maximum=100`,
`IsTabStop=False` and `IsHitTestVisible=False`. The form declares three
TextBlocks named `TextBlock_CraftPointValue`,
`TextBlock_QualityPointValue` and `TextBlock_HQRate`.

The local template dictionary has a style keyed
`Style_ProgressBar_TimerCommand` with target type `ProgressBar`.
Its `TimeOverSe` command trigger contains one `SoundPlayerAction` with
`FileNumber=38` and `Volume=100`. The same style declares
`StartLimitTimer` and `StopLimitTimer` command triggers.

These are static declarations. The measured inputs do not establish the
call that issues each timer command, when the action runs, or the audible
gain produced by this literal. The action property type and runtime consumer
are in `xivl-decomp:docs/resource/sound-effect-triggers.md`.
