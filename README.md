# GTA 6 hash database (GTA VI joaat names)

Grand Theft Auto VI (GTA 6) stores names as 32-bit joaat hashes: stats, items, vehicles, missions, save keys, radio
songs. This repository is a lookup table for them. It covers what each hash in a GTA VI story save stands for, how the
name was found and how sure it is, and one merged index of 1.15 million hashes from the community's GTA 6 name lists.
Everything is plain tab-separated text, sorted, one row per hash, so it works with any tool: grep, a spreadsheet,
Python or a modding tool.

Use it to read GTA 6 save files, name hashes in game data, or check a name before you use it. The save tables come
from [Save Garage](https://github.com/NotHGM/save-garage), a GTA VI story save editor for PS5, where every name was
checked against real saves.

## What's inside

### `data/save/`: the story save, decoded

Every hash that appears in a PS5 story save, named or not, with the evidence for each name.

| File | What it holds | Named |
|---|---|---|
| `stat_bases.tsv` | Stat names, the first part of a stat key such as `lifetimemoneyearned` | 316 of 386 |
| `stat_qualifiers.tsv` | Stat qualifiers: weapons, vehicles, places, activities, game modes | 2,507 of 3,763 (another 1,191 have the game's label, 62 a description) |
| `stat_owners.tsv` | Stat owners: the total, Lucia, Jason, missions, gang operations, arcade games | 233 of 239 |
| `items.tsv`, `slots.tsv` | Inventory item and slot IDs | 944 of 1,138 and 554 of 586 |
| `sections.tsv`, `json_keys.tsv` | The save's own sections and JSON keys (hashed as written, not lower-cased) | 64 of 82 and 610 of 843 |
| `stat_screen_labels.tsv` | Whole stat rows and what the game's stats screens call them | 393 rows |
| `text_ids.tsv` | IDs that are the key of their own on-screen text (discovery entries, radio stations, text messages, unlockables) | 693 |
| `suffix_text_ids.tsv` | Social media posts, news articles and accounts, whose text is keyed by the ID's name plus `_caption`, `_header` or `_handle` | 2,360 |
| `collectibles.tsv` | Keys of the collectible tables: hoops, street art, doubloons, flamingos, magazines, books, watches, magazine styles, cards | 1,012 |
| `vehicle_compendium.tsv` | Every base-model vehicle: model, the key the compendium uses (the hash of its game name), the page that counts it | 231 |
| `gang_operations.tsv` | The 44 gang locations: owner hash, gang, the name the map uses, and whether it counts for 100% | 44 |
| `missions_and_tasks.tsv` | Content IDs of story missions, optional tasks and side missions, with titles | 137 |
| `robbery_locations.tsv` | Robbery locations by type | 149 |

The columns that matter most:

- `confidence`:
  - **confirmed**: two independent proofs, such as a literal from a dump that also fits where it sits in the save, or a second hash.
  - **likely**: one structural fit from a search whose chance rate was measured with decoy hashes and found near zero.
  - **named**: from the earliest lists, before grades were kept.
  - **inferred**: a label taken from the game's own stats screens.
- `game_label`: the game's own text for the value, where its text table has one.
- `meaning`: for a hash whose real name is still unknown, what the value holds, worked out from how it behaves across many saves.
- `source`, `evidence`, `research_round`: how the name was found.

### `data/community/`: every known name, merged by hash

`hashes_0.tsv` to `hashes_f.tsv`, split by the first hex digit of the hash: 1,153,603 hashes with every name proposed
for them and where each came from. It merges the public GTA VI name lists (asm512, lynxnathan, tarekmania and
ahmed605's strings database), the names in DurtyFree's GTA VI data dumps (`durtyfree`, with its 210,645 model names)
and in Zia-ullah-khan's car spawn maps (`zia-ullah-khan`), and the names verified above (`save-garage`). A hash can
have several names. When one of them comes from `save-garage`, that name has been checked against real saves.

### `data/game/`: game data tables

`game_data.tsv` lists 4,743 hashes from the game's metadata tables, as dumped by DurtyFree: peds, vehicles, weapons,
ammo, pickups, animal tunings, ped capsules and navigation, doors, vehicle colours and plates, weapon accuracies and
damage modifiers. A name is given only when it hashes to the row's hash (887 rows). The other 3,856 hashes are still
unnamed: `other_names` shows any name the community index proposes for them (551 rows).

### `data/traffic/`: traffic and car spawns

Which kinds of vehicle the game spawns where, from Zia-ullah-khan's car spawn maps (read from the game's popcycle table
and zone volumes):

| File | What it holds |
|---|---|
| `areas.tsv` | 199 named areas with their hash, position, size and the traffic schedule they use |
| `schedules.tsv` | 137 traffic schedules: the weight of each vehicle category in each of the 12 time slots |
| `zones.tsv` | 200 zone volumes: schedule, source file, centroid, height and outline |

Most schedule hashes are still unnamed. If you find one, a contribution is welcome.

### `data/radio/`: the radio

| File | What it holds |
|---|---|
| `stations.tsv` | The 28 stations, with their keys |
| `song_names.tsv` | 1,658 song and recording names with their 32-bit and 29-bit hashes (audio uses both) |
| `tracklist.tsv` | The published track list by station |

`data/counts.json` has the size of every table.

## Looking things up

`tools/lookup.py` needs only Python 3:

```
python3 tools/lookup.py 0x5299e475           # a hash: every table that knows it
python3 tools/lookup.py lifetimemoneyearned  # a name: its hashes and where they appear
python3 tools/lookup.py --search robbery     # names, labels and titles containing a word
python3 tools/lookup.py --hash "Some Name"   # the joaat hashes of a string
```

Most names are hashed in lower case. The save's JSON keys and sections are hashed exactly as written, so the tool
prints both forms.

## How the save names were found

- **Name lists:** candidate names from the community lists, game text and dumps of other RAGE games were hashed and
  matched against the hashes in real saves.
- **Brute force:** word combinations and numbered families were searched. The last step of joaat can be undone, so a
  name's suffix can be added to a hash without knowing the name.
- **Decoys:** every search was also run against random hashes. A name is only kept when real hits clearly beat the
  decoy hits.
- **Behaviour:** names and meanings were checked against how each value changes across 20 saves of two playthroughs,
  and against the game's own stats screens on a PS5.

## Contributing

Found a new name or a wrong one? Add it to a file in `contributions/` and open a pull request; `tools/check_contribution.py` checks every hash against its name first. [CONTRIBUTING.md](CONTRIBUTING.md) explains the format, and the **New names** and **Wrong name** issue forms work too if you'd rather not open a pull request.

## Related

- [Save Garage](https://github.com/NotHGM/save-garage): edit a GTA VI story save on PS5 (money, ammo, stats, 100%
  completion and every value in the save), built on these names.

## License

MIT (`LICENSE`) for this repository's own work. The asm512, lynxnathan, tarekmania and ahmed605 name lists and the
radio catalog are MIT licensed too; their license texts are in `third_party/LICENSES.md`.

DurtyFree's GTA VI data dumps and Zia-ullah-khan's car spawn maps are published without a license. Only their names,
hashes and tables are used here, each marked with its source, and the MIT license here does not cover them. If you
wrote one of them and want it taken out or credited differently, open an issue.
