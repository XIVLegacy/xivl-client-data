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
- The decimal word lists were not matched against any consumer.
- The `12000_`, `skl_`, `empty` and `npc_` files were counted and not read.
- Motion payloads and control block records are outside this page.
