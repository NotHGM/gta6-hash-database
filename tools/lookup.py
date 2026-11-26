#!/usr/bin/env python3
"""Look up GTA VI hashes and names in this database.

  python3 tools/lookup.py 0x5299e475          a hash (with or without 0x): every table that knows it
  python3 tools/lookup.py moneyearned          a name: its hashes (lower-case and exact-case) and where they appear
  python3 tools/lookup.py --search robbery     names containing a word, in the save, radio, game and traffic tables
  python3 tools/lookup.py --hash "Some Name"   just the joaat hashes of a string

Only the Python standard library is used. Hashes are joaat (Jenkins one-at-a-time): stat, item and most game names
are hashed lower-case; save JSON keys and section names are hashed exactly as written."""
import csv, glob, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def joaat(s, lower=True):
    h = 0
    for c in (s.lower() if lower else s).encode('utf-8'):
        h = (h + c) & 0xffffffff
        h = (h + (h << 10)) & 0xffffffff
        h ^= h >> 6
    h = (h + (h << 3)) & 0xffffffff
    h ^= h >> 11
    return (h + (h << 15)) & 0xffffffff


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f, delimiter='\t')


def tables():
    for p in sorted(p for d in ('save', 'radio', 'game', 'traffic') for p in glob.glob(os.path.join(ROOT, d, '*.tsv'))):
        yield os.path.relpath(p, ROOT), p


def by_hash(h):
    hx = '%08x' % h
    found = []
    for name, p in tables():
        for r in rows(p):
            if any(v == hx for k, v in r.items() if k and ('hash' in k or k in ('compendium_key', 'key_hash', 'id', 'content_id', 'page_counter'))):
                found.append((name, {k: v for k, v in r.items() if v}))
    shard = os.path.join(ROOT, 'community', 'hashes_%x.tsv' % (h >> 28))
    if os.path.exists(shard):
        for r in rows(shard):
            if r['hash'] == hx:
                found.append(('community/' + os.path.basename(shard), r))
                break
    return found


def main(argv):
    if not argv:
        print(__doc__); return 1
    if argv[0] == '--hash':
        s = ' '.join(argv[1:])
        print('lower-case %08x   exact-case %08x' % (joaat(s), joaat(s, False))); return 0
    if argv[0] == '--search':
        word = ' '.join(argv[1:]).lower()
        for name, p in tables():
            for r in rows(p):
                if any(word in (v or '').lower() for k, v in r.items() if k in ('name', 'game_label', 'meaning', 'title', 'map_name', 'game_text', 'text_start', 'model', 'other_names', 'category', 'schedule_name')):
                    print('%-34s %s' % (name, {k: (v if len(v) <= 90 else v[:89] + '…') for k, v in r.items() if v and k not in ('source', 'evidence', 'research_round')}))
        return 0
    q = argv[0]
    m = re.fullmatch(r'(?:0x)?([0-9a-fA-F]{8})', q)
    hashes = [int(m.group(1), 16)] if m else sorted({joaat(q), joaat(q, False)})
    if not m:
        print('%s -> lower-case %08x, exact-case %08x' % (q, joaat(q), joaat(q, False)))
    for h in hashes:
        res = by_hash(h)
        print('%08x: %s' % (h, 'not found' if not res else ''))
        for name, r in res:
            print('  %-34s %s' % (name, r))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
