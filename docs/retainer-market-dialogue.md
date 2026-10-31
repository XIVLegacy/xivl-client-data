# Retainer market dialogue

The retail dialogue contains an aggregate sales report during the owner's
absence and describes gil from sold wares as belonging to the owner. These
are authored-text findings. They do not establish an observed transaction,
logged-out owner, balance destination, automatic credit or collection request.

## Authored service and sale reports

Source locators use the CSV row key and named English column `1`. That is
zero-based CSV field index `2`, after the row-key field and Japanese column.

| Source | English text establishes | Boundary |
| --- | --- | --- |
| `csv/ordinaryRetainer.csv`, row `540`, physical line `541` | A supplied number of sales is reported during the owner's absence. | Absence is not an explicit offline or logout state. |
| `csv/ordinaryRetainer.csv`, row `546`, physical line `547` | A sold-wares report describes the resulting gil as the owner's. | No currency-item destination, balance mutation or collection operation is specified. |
| `csv/ordinaryRetainer.csv`, rows `502-546`, physical lines `503-547` | The 45 aggregate sold-count report variants each contain number token `022003e80203`. | They do not identify a detailed sale-history request, reply schema, per-item ledger, timestamp, buyer identity or price. |
| `csv/populaceRetainerManager.csv`, rows `151/169`, physical lines `153/171` | Retainers manage bazaars while the owner is away adventuring. | No login-state predicate or completed buyer transfer is observed. |
| `csv/populaceRetainerManager.csv`, rows `166/176`, physical lines `168/178` | The warning says bell summoning a retainer from market closes that retainer's bazaar. | Runtime closure sequencing is not established by the text. |

The aggregate report's number token is retained as an exact text locator.
This finding does not assign it a network-field offset or infer a producer's
value, argument type or transaction count unit. NPC references to books or
records do not by themselves establish a sale-history interface.

Offline-owner purchasability still requires a retained transaction with the
seller player's session state established over the purchase interval.
Proceeds destination and collection require the sale-to-balance and
collection-to-mutation joins. A detailed sale-history contract requires an
identified opening/request, complete reply and attributable displayed row.

## Source identity and verification

`manifests/tables.json` pins both members from retail 1.23b extraction
`2012.09.19.0001`:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `ordinaryRetainer.csv` | `224893` | `0a0cf8c20f8d3263c6efa223433cd707f6dfeff63b5309052a20aa69aeb56401` |
| `populaceRetainerManager.csv` | `69200` | `afeddb2538dd2e4e01abdb3466dfe6d467e12cc266d12767414276d404fca1ec` |

The source archive declared by `manifests/private_csv_corpus.json` matched
`70110686` bytes and SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
Python 3.12.0 standard-library `zipfile`, `csv` and `hashlib` authenticated
the archive and two members before parsing the selected English cells.
Focused row, column, wording and number-token checks passed. The checks
establish the shipped text and source identity; they do not establish runtime
display, a server request/reply, an authoritative transaction or settlement.
