#!/usr/bin/env python3
"""Check contribution files before opening a pull request.

  python3 tools/check_contribution.py contributions/my-names.tsv [more files...]
  python3 tools/check_contribution.py            (checks every file in contributions/)

For every row it checks that the hash really is the joaat of the name (lower-case, exact-case or 29-bit, as the row
says), that the table is one of the known ones, and that nothing is listed twice. It also says which names are new,
which are already known, and which disagree with a name the database already has. Only the Python standard library
is used. Paste the summary it prints into your pull request."""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
TABLES = {'stat_base', 'stat_qualifier', 'stat_owner', 'item', 'slot', 'section', 'json_key', 'collectible', 'vehicle',
          'mission', 'text_key', 'audio', 'other'}
CASES = {'lower', 'exact', 'hash29'}
COLUMNS = ['hash', 'name', 'table', 'hash_case', 'evidence', 'source', 'game_version']
SAVE_TABLES = {'stat_base': 'stat_bases', 'stat_qualifier': 'stat_qualifiers', 'stat_owner': 'stat_owners', 'item': 'items',
               'slot': 'slots', 'section': 'sections', 'json_key': 'json_keys'}


def joaat(s, lower=True):
    h = 0
    for c in (s.lower() if lower else s).encode('utf-8'):
        h = (h + c) & 0xffffffff
        h = (h + (h << 10)) & 0xffffffff
        h ^= h >> 6
    h = (h + (h << 3)) & 0xffffffff
    h ^= h >> 11
    return (h + (h << 15)) & 0xffffffff


def hash_of(name, case):
    if case == 'exact':
        return joaat(name, False)
    h = joaat(name)
    return h & 0x1fffffff if case == 'hash29' else h


def known_names():
    """hash -> {name: where} from the save tables and the community index (read lazily, per shard)."""
    save = {}
    for t in SAVE_TABLES.values():
        p = os.path.join(ROOT, 'data', 'save', t + '.tsv')
        if os.path.exists(p):
            with open(p, encoding='utf-8', newline='') as f:
                for r in csv.DictReader(f, delimiter='\t'):
                    if r.get('name'):
                        save.setdefault(r['hash'], {})[r['name']] = '%s (%s)' % (t, r.get('confidence') or 'named')
    return save


_shards = {}


def community(hx):
    k = hx[0]
    if k not in _shards:
        p = os.path.join(ROOT, 'data', 'community', 'hashes_%s.tsv' % k)
        _shards[k] = {}
        if os.path.exists(p):
            with open(p, encoding='utf-8', newline='') as f:
                for r in csv.DictReader(f, delimiter='\t'):
                    _shards[k][r['hash']] = set((r.get('names') or '').split(' | '))
    return _shards[k].get(hx, set())


def check(path, save):
    errors, warnings, new, known = [], [], 0, 0
    seen = set()
    with open(path, encoding='utf-8', newline='') as f:
        lines = [l for l in f if l.strip() and not l.lstrip().startswith('#')]
    reader = csv.DictReader(lines, delimiter='\t')
    if reader.fieldnames is None or [c.strip() for c in reader.fieldnames] != COLUMNS:
        return ['%s: the first line must be the header: %s' % (path, '\t'.join(COLUMNS))], [], 0, 0, 0
    rows = 0
    for i, r in enumerate(reader, start=2):
        rows += 1
        r = {k: (v or '').strip() for k, v in r.items()}
        where = '%s line %d' % (os.path.basename(path), i)
        hx = r['hash'].lower().removeprefix('0x')
        if not re.fullmatch(r'[0-9a-f]{8}', hx):
            errors.append('%s: hash "%s" is not 8 hex digits' % (where, r['hash'])); continue
        if not r['name']:
            errors.append('%s: the name is empty' % where); continue
        if r['table'] not in TABLES:
            errors.append('%s: table "%s" is not one of %s' % (where, r['table'], ', '.join(sorted(TABLES)))); continue
        case = r['hash_case'] or 'lower'
        if case not in CASES:
            errors.append('%s: hash_case "%s" is not lower, exact or hash29' % (where, case)); continue
        got = hash_of(r['name'], case)
        if got != int(hx, 16):
            hint = [c for c in CASES if hash_of(r['name'], c) == int(hx, 16)]
            errors.append('%s: %s hashes to %08x (%s), not %s%s' % (where, r['name'], got, case, hx,
                                                                   ' (it matches as %s)' % hint[0] if hint else ''))
            continue
        if not r['evidence']:
            errors.append('%s: say where you saw the name or why it fits (evidence)' % where); continue
        if (hx, r['name']) in seen:
            warnings.append('%s: %s %s is listed twice' % (where, hx, r['name'])); continue
        seen.add((hx, r['name']))
        mine = save.get(hx, {})
        if r['name'] in mine or r['name'] in community(hx):
            known += 1
        else:
            new += 1
            if mine:
                warnings.append('%s: the database already names %s as %s; say in the evidence why %s is right' %
                                (where, hx, ', '.join('%s [%s]' % kv for kv in mine.items()), r['name']))
    return errors, warnings, rows, new, known


def main(argv):
    files = argv or sorted(p for p in glob.glob(os.path.join(ROOT, 'contributions', '*.tsv')) if not os.path.basename(p).startswith('_'))
    if not files:
        print('No contribution files. Copy contributions/_template.tsv to contributions/<your-file>.tsv and add your rows.')
        return 1
    save = known_names()
    bad = 0
    for p in files:
        errors, warnings, rows, new, known = check(p, save)
        print('%s: %d rows, %d new, %d already known, %d errors, %d warnings' % (os.path.relpath(p, ROOT), rows, new, known, len(errors), len(warnings)))
        for e in errors:
            print('  error:', e)
        for w in warnings:
            print('  note:', w)
        bad += len(errors)
    print('RESULT: %s' % ('OK' if not bad else 'fix the errors above'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
