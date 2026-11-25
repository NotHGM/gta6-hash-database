# Contributing names

Found the name behind a GTA 6 hash, or spotted a wrong one? Add it here. Every name helps: stats, items, vehicles,
missions, save keys, audio, map places, anything the game hashes.

## The short version

1. Fork this repository.
2. Copy `contributions/_template.tsv` to `contributions/<your-name-or-topic>.tsv`, for example
   `contributions/weapons-attachments.tsv`.
3. Add one row per name (the columns are below).
4. Run the checker and fix anything it reports:
   ```
   python3 tools/check_contribution.py contributions/<your-file>.tsv
   ```
5. Open a pull request and paste the checker's summary into it.

Please don't edit the files in `data/`. They are generated from the research and the contributions, so a hand edit
there is overwritten at the next rebuild. Your file in `contributions/` is merged in instead.

Don't have time for a pull request? Open an issue with the **New names** or **Wrong name** form instead.

## The columns

The file is tab-separated, one row per name. Lines starting with `#` are ignored.

| Column | What to put |
|---|---|
| `hash` | The 32-bit hash, 8 hex digits (`d5188146` or `0xd5188146`) |
| `name` | The name that hashes to it, exactly as the game spells it |
| `table` | `stat_base`, `stat_qualifier`, `stat_owner`, `item`, `slot`, `section`, `json_key`, `collectible`, `vehicle`, `mission`, `text_key`, `audio` or `other` |
| `hash_case` | `lower` (most names), `exact` (save JSON keys and section names, hashed as written), or `hash29` (audio names that use the low 29 bits) |
| `evidence` | Where you saw the hash and why the name fits. For example: "row of the stats section, owner charlucia, shown on the stats screen as MONEY EARNED" |
| `source` | A link, a file or tool name, or "own research" |
| `game_version` | The build you checked it on, for example `PS5 1.0` or `Xbox 1.0.2.1` |

Not sure which table? Use `other` and say what it is in the evidence.

## What makes a good contribution

- **The hash has to match the name.** The checker computes joaat for you, so a typo or the wrong case is caught
  before anyone reviews it.
- **Say how you know.** A name that only matches the hash can be a coincidence: with a million names, some collide by
  chance. A name backed by where the value sits, or by what the game shows, is what gets a name accepted.
  - **Strong evidence:** the name appears in game files or scripts next to the hash; the value behaves like the name
    says across saves; the game's own screen shows it.
  - **Weak on its own:** "it was the only match in my word list". Still welcome; it's marked weak until confirmed.
- **Correcting a name already in the database:** add the right name and explain in the evidence why the current one
  is wrong. The checker points out names that disagree.
- **Keep it to names and short labels.** Please don't add dumps of the game's text, dialogue or other files.

## How it's reviewed

The maintainer re-runs the checker, looks at the evidence, and merges the file. At the next rebuild your names go into
`data/community/`, credited to your file. A name that fills a gap in `data/save/` appears there too, marked
`contributed` until it's confirmed against real saves.

By contributing you agree that your contribution is released under this repository's MIT license.
