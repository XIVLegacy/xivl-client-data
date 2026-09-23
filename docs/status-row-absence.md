# Status row absence

No row keyed `230116` occurs in either pinned status table. The exact first
column key was checked across each complete table member.

| Table | SHA-256 in `manifests/tables.json` |
| --- | --- |
| `status.csv` | `3b09a76123b0fd8aba320dc5513e8182820fef409cf9d40f0b522b10b11d02ec` |
| `xtx_status.csv` | `60eca3b76d1d9799589d9059adeb1e7c3d142e07609a1ad0a053c5e75d9b96ee` |

This records table membership only. It does not establish how a status ID is
received or generated, how the client handles it at runtime, or any server-side
effect or presentation behavior.
