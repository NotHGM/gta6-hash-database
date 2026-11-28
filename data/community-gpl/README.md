# GPL-3.0 names (`data/community-gpl/`)

Names from sources published under the GNU General Public License v3.0. The GPL doesn't allow them in the MIT index
in `data/community/`, so they are kept here, under GPL-3.0 (`LICENSE` in this folder). Everything else in this
repository stays MIT.

`hashes.tsv` lists each hash with every name these sources propose for it, where each came from, and `in_mit_index`
(`yes` when the MIT index has the hash too, with names of its own).

| Source | What | How it is hashed |
|---|---|---|
| [holdmysocks/SixNG](https://github.com/holdmysocks/SixNG) (`sixng`, commit 67fc274) | `crates/sixng-core/src/names_exe.txt`: meta field and struct names from the game executable's parser table; `crates/sixng-core/src/enum_values.txt`: enum value names | joaat of the name as written |
| [Two-Play/openRAGE](https://github.com/Two-Play/openRAGE) (`two-play-openrage`, commit 36395ab) | `crates/rage-formats/src/meta_names.txt`: metadata field and type names (its header says they come from CodeWalker's MetaNames) | a bare name hashes as written; `name hash` lines give the hash |
| [tarekmania/gta6-namehash](https://github.com/tarekmania/gta6-namehash) (`tarekmania-confirmed`, commit 17f4511) | `confirmed.json`, its confirmed layer from 28 November 2026, which it builds partly from SixNG | the hash it gives |

Credit for each name goes to its source, and the GPL-3.0 terms of those sources apply to this folder. If you wrote one
of them and want it taken out or credited differently, open an issue.
