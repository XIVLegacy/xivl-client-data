# Cut scene DataSet entries and motion banks

A cut scene names each motion it plays in the name table of its scheduler.
This page records where the installed files of client extraction
`2012.09.19.0001` hold the motion data of those names: inside the scene
file, in the `DataSet` directory beside it, and in the shared `client/cut/mot`
tree. It measures names and containers only. Which of these places the
client reads for a given actor is not established here.

The native side of a motion request is recorded in
`xivl-decomp:docs/resource/motion-resource-request.md`, "Entry and MCB
availability" and "Type/name interface and resource-provider boundary". A
RaptureMotionClip resolves its name from the scheduler name table
(`xivl-decomp:docs/resource/combat-motion-name-provider.md`,
"ResourceReference and serialized provider") and asks the actor's resource
interface for the control block and the motion of that name. The provider's
roots and search order are not established there.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`. No file bytes are reproduced here.

A scene file is `client/cut/<scene>/<scene>`. It starts with `PWIB`, and its
big-endian u32 at `+0x08` is the offset of an `SEDB` `RES ` directory. The
directory framing is that of `xivl-tools:docs/formats/sedb-res.md`, "RES
subresource directory": the entry count at `+0x30`, the name table offset
at `+0x34`, 16-byte entries from `+0x40`, and one NUL-terminated name per
entry. An entry whose payload starts with `SEDBRES ` is a nested directory
and was walked the same way.

The scheduler is the entry that starts with `SEDB` `SCB`. Its actor records
and its `RIDTBL` name table were read with the layouts of
`xivl-decomp:docs/resource/cut-scheduler-clip-layout.md`, "Resource header
and directory", and the name table formula of the provider page above. A
ProxyActor record carries its numeric name input as the u32 at record
`+0x24` (`xivl-decomp:docs/resource/cut-proxy-actor-names.md`, "Selected
record and interfaces").

Files read as exemplars:

| File below `client/cut` | Bytes | SHA-256 |
| --- | ---: | --- |
| `man0g000/man0g000` | 2599264 | `884d95a67b13aa4b2f50ca78ecabb2533673357face7ff021e8ae3ce137d75f0` |
| `man0g000/DataSet/10000_c001` | 903232 | `4a49a243e295b01aa0b91899ce608672b41c0b9a1e2845e0f87f8771c298206f` |
| `man0g000/DataSet/10000_c001f002` | 145168 | `9415404660ca001f63ece36a6d06a4f0f853f80c78290076829e6651dd55bd1e` |
| `man0g005/man0g005` | 57248 | `6fee52225e98542896576c38286fae9220e11ec45b5fc2cd3c0723b375c24c2d` |
| `man0g005/DataSet/10000` | 11 | `e8bcb07cdc9df726f26c289105aba110379a98d86f9361b6d5b6585c743274e6` |
| `mot/c001/cbfp_u_ude` | 19712 | `d52ac057d6faecc704fac26ef97e04795ee277e1bfb8a5323f13cb0bd8373320` |

## Entries of a scene file

The top directory of `man0g000/man0g000` holds these entries, in order:
`\CommonResource`, `DataSet\cameraactor_roo`, thirteen entries named
`DataSet\<N>`, `bin\man0g000`, `RESOURCE_TYPE` and `RESOURCE_ID`. The
scheduler is `bin\man0g000`. Each `DataSet\<N>` entry is a nested
directory.

The scheduler holds 21 ProxyActor records. Their `+0x24` values are 10000,
11000 to 11005, 11052, 11080 to 11087, 11089 to 11093. The thirteen nested
directories carry the decimal text of thirteen of those values: 11000,
11001, 11002, 11003, 11004, 11005, 11052, 11085, 11086, 11089, 11090, 11092
and 11093. No entry is named for 10000.

A nested directory holds its motion data as pairs of entries with the same
last name component:

| Entry name ends in | Payload starts with |
| --- | --- |
| `mcc\bin\<name>` | `SEDB` `MCB` NUL |
| `miga\bin\<name>` | `SEDB` `mtb` NUL |

`DataSet\11000` holds three pairs, named `eb_man0g000a15x`,
`eb_man0g000a17x` and `ef_man0g000a17x`. `DataSet\11003` holds one pair,
`eb_man0g000d05x`. The directories 11052 and 11093 hold their pairs under
longer entry paths that end the same way. The directories 11085, 11086,
11089, 11090 and 11092 hold only `SEDB` `ACB` payloads. Each nested
directory ends with a `RESOURCE_TYPE` and a `RESOURCE_ID` entry.

Every name of an `MCB` or `mtb` entry in the thirteen nested directories
is an entry of the scheduler name table.

## Files beside a scene file

`man0g000/DataSet` holds 28 files. Each name is `10000_c<NNN>` or
`10000_c<NNN>f<NNN>`. Each is a `PWIB` file with the same directory framing.

| File | Pairs | Entry paths | Names |
| --- | ---: | --- | --- |
| `10000_c001` | 19 | `mcc\base\b001\bin\<name>`, `miga\base\b001\bin\<name>` | the 19 distinct `cb_` names of the scheduler name table |
| `10000_c001f002` | 10 | `mcc\fac\f002\bin\<name>`, `miga\fac\f002\bin\<name>` | the 10 distinct `cf_` names of the scheduler name table |

The `c001` and `f002` parts match the installed directories
`client/chara/pc/c001` and `client/chara/pc/c001/kao/f002`.

Across `client/cut`, 665 scene directories hold a `DataSet` directory, with
5061 files in all:

| Name shape | Files |
| --- | ---: |
| decimal digits only | 4465 |
| `<N>_<rest>` | 587 |
| `skl_` prefix | 5 |
| `empty` | 3 |
| `npc_` prefix | 1 |

Of the 587, 503 start with `10000_` and 84 with `12000_`.

A file named by decimal digits only is not a directory file. Every byte of
all 4465 has its high bit set. With that bit cleared, each file reads as
ASCII letters, digits, underscores and spaces. `man0g005/DataSet/10000` is
11 bytes and holds one such word.

## Shared motion tree

`client/cut/mot` holds 31 directories: `c001` to `c010`, `c021` to `c025`,
`m041`, `m502`, `m701`, `m702`, `m703`, `m708`, `m709`, `m854`, `m901` to
`m905` and `m910` to `m912`.

`mot/c001` holds 318 files, each a `PWIB` file named by a motion name.
`mot/c001/cbfp_u_ude` holds one pair, `mcc\base\b001\bin\cbfp_u_ude` and
`miga\base\b001\bin\cbfp_u_ude`, with the payload tags of the table above.

The scheduler name table of `man0g005/man0g005` lists `cbfp_u_ude`. The
top directory of that scene file holds `DataSet\11000`, `DataSet\11001`,
`bin\man0g005`, `RESOURCE_TYPE` and `RESOURCE_ID`, with no entry named for
10000. The scene's `DataSet` directory holds the single file `10000`. So
neither place of that scene holds motion data named `cbfp_u_ude`, and
`mot/c001` does.

## Proxy word files of man0u005

`client/cut/man0u005/DataSet` holds ten word files, named 10000, 11000 to
11007 and 11010. With the high bit of every byte cleared, each reads as
motion names separated by single spaces, with a trailing space.

| File | Bytes | SHA-256 | Names |
| --- | ---: | --- | --- |
| `10000` | 25 | `5217188d8ea29e1b3f6fc657b9fe0e64aae41779a6b18fd6e10f412af3fa0dfc` | `cbfm_swalk_ed`, `cbfp_u_ude` |
| `11000` | 48 | `26692086d6230e255c179edd6f7f12b374d2711c5c8ee8903e413ced2cb480df` | `cbfp_u_yubi02`, `cbfm_talk_w`, `cbfp_u_ude`, `cbfm_smile` |
| `11001` | 66 | `92b076d069c934a75b065f5e9dc157f2251368c6a2f1a8caf41fb0dc9c6692ed` | `cbfm_talk_big`, `cbfp_u_talk03`, `cbfm_smile_g`, `cbfp_u_hands`, `cbfm_talk_h` |
| `11002` | 12 | `dede6329a13fba866f0b95bb7bdb37bdefc65ed9107171b8bc0bbcc6530b3fb4` | `cbfm_hima02` |
| `11003` | 11 | `ff64f9c5da0cd53ba2ab802d8356f298f31710232a98db0a0204f2afef7dcffd` | `cbem_upset` |
| `11004` | 30 | `ea4b3a90cae31df79533b6e124d51d06fe706877e3e18f4858e88b136bab3104` | `cbfm_bwalk_mv`, `cbfm_talk_ang02` |
| `11005` | 14 | `85ad91639bbc43835383f41ba0ef707ee6926d29ec6d10d8dcd044df5deddfaf` | `cbem_blowkiss` |
| `11006` | 13 | `02d2cec2157638e55c4e8e9a0169f9a5ffa1d359037fb1bccd9955aef9f6dbf1` | `cbem_lookout` |
| `11007` | 21 | `5b345b59a2a447d491e5de4ec1ae38f48c35850063eff81aeaf3fe989392a270` | `cbem_cheer`, `cbem_clap` |
| `11010` | 33 | `508deaf4220253a15c90166641fd5d291d1f0e8bb027b703e1e6aff9b59ff8c9` | `cbfp_u_ude`, `cbfa_not`, `cbfa_look_lr` |

Only `11003` lists `cbem_upset`.

## cbem names in the shared tree

Each of `mot/c001` to `mot/c009` holds 92 files whose names start with
`cbem_`, `cbem_upset` among them. `mot/c010`, `mot/c021` to `mot/c025` and
every `m` directory hold none.

| File below `client/cut/mot` | Bytes | SHA-256 |
| --- | ---: | --- |
| `c001/cbem_upset` | 40560 | `2780caaf04e40d741af4298a15f3859c4c33964e95f714b961aa91a6c4b4209c` |
| `c002/cbem_upset` | 51136 | `53543b17d012467b2cf1c290458c67cf0558d0ae353d7e1ad1ffc121af4ce453` |
| `c003/cbem_upset` | 51904 | `9b45db2be2742294c31303576dd912923da6fff3ded5286e81451ae311c03c0f` |
| `c004/cbem_upset` | 53456 | `ddaf677f469f1d4e7273d5292d06dc1bd32f6779ba8f91ae6e5c718084296574` |
| `c005/cbem_upset` | 38432 | `c8cea0ece60dcc1a1af0fd380050fbf0115903d0497c68f02439ff2b713722c2` |
| `c006/cbem_upset` | 39328 | `b6bd5345c7a5f7f8138475647f187a4b12b5c928d5f8800c3e08039c4327a068` |
| `c007/cbem_upset` | 73424 | `0faa38cdb2ec6e1471e317fc94dc12fb612b5cae743e886b3ab9934e357a648c` |
| `c008/cbem_upset` | 38816 | `c38c43e1073b055dffc9f9572d0e01741c3b06eb872224cb3005fe02118b39b2` |
| `c009/cbem_upset` | 76288 | `4c7b95d4117ae5075f470503d66709c484af27171b0db7683de951086a8425f0` |

Each starts with `PWIB`. The native loader that builds
`/client/cut/mot/<model directory>/<name>` paths, and its directory rule,
are `xivl-decomp:docs/resource/cut-motion-tree-loader.md`. Under that rule
a model word 22 reads `mot/c022`, which holds no `cbem_upset`.

## Reading

For one scene the three places partition the names by prefix. The `eb_` and
`ef_` names of numbered proxies sit in the scene file under
`DataSet\<N>`. The `cb_` and `cf_` names of proxy 10000 sit in the files
`DataSet/10000_<model>` and `DataSet/10000_<model><face>`. A standard motion
name with no scene part sits in `mot/<model>`.

This is a layout of the installed files. It is INFERRED, not traced, that
the client registers these entries with the actor's resource provider when
a cut binds its ProxyActors, and that it selects the `10000_` file by the
model of the bound character.

## Limits

- Only `man0g000`, `man0g005` and `mot/c001` were read entry by entry. The
  name shape counts cover every `DataSet` directory.
- The decimal word lists were not matched against any consumer. Which
  model each `man0u005` proxy binds is not established here.
- The `12000_`, `skl_`, `empty` and `npc_` files were counted and not read.
- Motion payloads and control block records are outside this page.
