"""Keeps presets meaning what they meant when an element's knobs change.

A preset stores each knob as a 0-1 value, in order (params[4k+3]). Change a
line in an element's parameter block and every stored value is read by the new
line. element_migrations.py lists, for each such change, what should happen to
the stored values. migrate() applies the entries a database hasn't had yet: to
the element's own presets, to the copies inside channel and global presets and
to state_backup.pkl. It remembers them in the database's migrations table. The
core calls it at startup, so new code never reads old presets.

    python3.12 migrations.py                   what the pending entries would change
    python3.12 migrations.py examples          the same for every example
    python3.12 migrations.py new g_cube [rev]  write an entry for g_cube's changes
                                               since the last commit (or rev)
"""
import importlib
import json
import os
import pickle
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from collections import Counter

# === steps: what an entry does to one element's knobs ===
# A step gets the knobs as rows [label, name, display, value] and changes them
# in place. Indices count from 0 and refer to the rows as the previous step left
# them. The element rewrites label and display on the first frame after a
# preset loads, so only the value (and a new knob's name) matters.

GRID = [i/1000 for i in range(1001)]


def distance(a, b):
    """How far apart two results of a parameter line are. Options only match exactly."""
    if a == b:
        return 0
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b)
    return float('inf')


def keep(k, old, new):
    """Knob k: store the value that makes the new line give what the old line gave."""
    results = []

    def step(rows, report):
        m = rows[k][3]
        want = old(m)
        if new(m) == want:
            return
        if not results:
            results.extend(new(n) for n in GRID)
        best = min(range(len(GRID)), key=lambda i: (distance(results[i], want), abs(GRID[i] - m)))
        # a smooth line falls between two grid points, look closer
        close = [min(max(GRID[best] + j/100000, 0), 1) for j in range(-100, 101)]
        n = min(close, key=lambda x: (distance(new(x), want), abs(x - m)))
        miss = distance(new(n), want)
        if miss == float('inf'):
            raise ValueError(f'knob {k}: {want!r} is not an option of the new line any more. '
                             'Write the old line with the option it becomes in its place.')
        numbers = [r for r in results if isinstance(r, (int, float))]
        if miss > 1e-3*(max(numbers) - min(numbers) if numbers else 0):
            report['clipped'] += 1
        rows[k][3] = n
    return step


def change(k, fn):
    """Knob k: store fn(stored value)."""
    def step(rows, report):
        rows[k][3] = fn(rows[k][3])
    return step


def derive(k, fn):
    """Knob k: store fn(all stored values), for a knob that depends on others."""
    def step(rows, report):
        rows[k][3] = fn([row[3] for row in rows])
    return step


def insert(k, name, value):
    """A new knob at k. Old presets get value, or fn(all stored values) if it's a function."""
    def step(rows, report):
        assert k <= len(rows), f'insert at {k}, but there are only {len(rows)} knobs'
        v = value([row[3] for row in rows]) if callable(value) else value
        rows.insert(k, [name, name, '', v])
    return step


def remove(k):
    """Knob k is gone."""
    def step(rows, report):
        del rows[k]
    return step


def move(k, to):
    """Knob k moves to position to, the knobs in between shift by one."""
    def step(rows, report):
        row = rows.pop(k)
        assert to <= len(rows), f'move to {to}, but there are only {len(rows) + 1} knobs'
        rows.insert(to, row)
    return step


# === applying entries ===

def elements_in(data):
    """The elements in a preset or a state: the preset itself, or every one a channel, global preset or state carries."""
    if isinstance(data, dict):
        if 'params' in data:
            yield data
        else:
            for value in data.values():
                yield from elements_in(value)


def apply(entry, data, report):
    """Runs one entry over every copy of its element in data. True if anything changed."""
    _, element, steps = entry
    changed = False
    for found in elements_in(data):
        if found['name'] != element:
            continue
        params = found['params']
        rows = [params[i:i+4] for i in range(0, len(params), 4)]
        for step in steps:
            step(rows, report)
        found['params'] = [x for row in rows for x in row]
        changed |= found['params'] != params
    return changed


def run(db, entries):
    """Applies entries in order to the presets in db, in memory.

    Returns a report per entry and the presets that changed, as {id: data}."""
    presets = [(id, kind, name, json.loads(data)) for id, kind, name, data in db.execute(
        'SELECT p.id, e.type, p.name, p.data FROM presets p JOIN elements e ON e.id = p.element_id')]
    reports, touched = [], {}
    for entry in entries:
        report = Counter()
        for id, kind, name, data in presets:
            if not any(found['name'] == entry[1] for found in elements_in(data)):
                continue
            report[kind] += 1
            try:
                if apply(entry, data, report):
                    report['changed'] += 1
                    touched[id] = data
            except Exception as e:
                e.add_note(f'in the {kind} preset {name!r}, migration {entry[0]!r}')
                raise
        reports.append((entry, report))
    return reports, touched


def show(reports):
    for (title, element, _), report in reports:
        kinds = ', '.join(f'{report[kind]} {kind}' for kind in ('generator', 'effect', 'channel', 'global') if report[kind])
        total = sum(report[kind] for kind in ('generator', 'effect', 'channel', 'global'))
        print(f'{title}\n    {total} presets hold {element}' + (f' ({kinds})' if kinds else ''))
        if total:
            print(f"    values change in {report['changed']}" +
                  (f", {report['clipped']} values were out of the new range and got the nearest one" if report['clipped'] else ''))


def applied(db):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name = 'migrations'").fetchone():
        return set()
    return {name for (name,) in db.execute('SELECT name FROM migrations')}


def pending(db):
    from element_migrations import MIGRATIONS
    names = [entry[0] for entry in MIGRATIONS]
    assert len(set(names)) == len(names), 'two migrations have the same name'
    done = applied(db)
    return [entry for entry in MIGRATIONS if entry[0] not in done]


def dump(data):
    # the same compact form db_manager.save_preset writes
    return json.dumps(data, indent=None, separators=(',', ':'))


def migrate(db_path='l3d.db', backup_path='state_backup.pkl'):
    """Applies the entries this database hasn't had yet. Copies the database first."""
    db = sqlite3.connect(db_path)
    todo = pending(db)
    if not todo:
        db.close()
        return
    copy = f'{db_path}.before-{time.strftime("%Y-%m-%d-%H%M%S")}'
    shutil.copy(db_path, copy)

    reports, touched = run(db, todo)
    for id, data in touched.items():
        db.execute('UPDATE presets SET data = ? WHERE id = ?', (dump(data), id))
    db.execute('CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY, applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    db.executemany('INSERT INTO migrations (name) VALUES (?)', [(entry[0],) for entry in todo])
    db.commit()
    db.close()

    # Reboot Core restores this, and it holds copies of the elements too
    if os.path.exists(backup_path):
        with open(backup_path, 'rb') as f:
            state = pickle.load(f)
        for entry in todo:
            apply(entry, state, Counter())
        with open(backup_path, 'wb') as f:
            pickle.dump(state, f)

    print(f'[migrations] database copied to {copy}')
    show(reports)


# === writing a new entry ===

BLOCK = re.compile(r'# === PARAMETERS START ===\n(.*?)# === PARAMETERS END ===', re.S)
MARKER = '    # new entries go above this line\n'


def knobs(source):
    """The knob lines of a parameter block in knob order, as [(name, expression of m)]."""
    found = {}
    for line in BLOCK.search(source).group(1).splitlines():
        indices = set(re.findall(r'args\[(\d+)\]', line))
        if not indices:
            continue
        assert len(indices) == 1, f'this line reads two knobs, write the entry by hand: {line.strip()}'
        target, expression = line.split('=', 1)
        k = int(indices.pop())
        assert k not in found, f'knob {k} is read by two lines, write the entry by hand'
        found[k] = (target.strip().removeprefix('self.'), re.sub(r'args\[\d+\]', 'm', expression).strip())
    assert sorted(found) == list(range(len(found))), f'knobs {sorted(found)} have a gap'
    return [found[k] for k in range(len(found))]


def new(element, rev='HEAD'):
    import element_migrations
    path = f"{'generators' if element.startswith('g_') else 'effects'}/{element}.py"
    now = open(path).read()
    before = subprocess.run(['git', 'show', f'{rev}:./{path}'], capture_output=True, text=True, check=True).stdout
    old, current = knobs(before), knobs(now)
    if BLOCK.sub('', before) != BLOCK.sub('', now):
        print('Code outside the parameter block changed as well. That is not looked at here: '
              'if it changes what a knob means, describe the knob with keep() by hand.\n')

    old_names = [name for name, _ in old]
    new_names = [name for name, _ in current]
    for name in [n for n in new_names if n not in old_names]:
        gone = [n for n in old_names if n not in new_names]
        if gone:
            answer = input(f"'{name}' is new. Is it one of {', '.join(gone)}, renamed? Its old name, or enter: ").strip()
            if answer:
                old_names[old_names.index(answer)] = name
    old_lines = dict(zip(old_names, [expression for _, expression in old]))

    # removed knobs first, then walk the new order moving and inserting
    rows, steps = list(old_names), []
    for k in reversed(range(len(rows))):
        if rows[k] not in new_names:
            steps.append(f'remove({k}),  # {rows[k]}')
            del rows[k]
    for k, name in enumerate(new_names):
        if name not in rows:
            value = float(input(f"Knob value (0-1) old presets get for the new '{name}': "))
            steps.append(f"insert({k}, '{name}', {value}),")
            rows.insert(k, name)
        elif rows.index(name) != k:
            steps.append(f'move({rows.index(name)}, {k}),  # {name}')
            rows.insert(k, rows.pop(rows.index(name)))

    by_hand = False
    for k, (name, expression) in enumerate(current):
        if name not in old_lines or old_lines[name] == expression:
            continue
        # these are lines of the element's own source, which the core runs anyway
        for line in (old_lines[name], expression):
            try:
                eval(f'lambda m: {line}', vars(element_migrations))(0.5)
            except (NameError, AttributeError) as e:
                sys.exit(f"'{line}' uses something defined outside the line ({e}). Write the value into the line.")
        print(f'\n{name}\n    old: {old_lines[name]}\n    new: {expression}')
        answer = input('[k]eep what presets look like, [s]ame knob value, or [e]dit by hand? ').strip()
        if answer == 'k':
            steps.append(f'keep({k}, old=lambda m: {old_lines[name]}, new=lambda m: {expression}),')
        elif answer == 'e':
            steps.append(f'change({k}, lambda m: TODO),  # {name}, old: {old_lines[name]}  new: {expression}')
            by_hand = True

    if not steps:
        print('Nothing to migrate: presets read the same.')
        return
    title = f"{time.strftime('%Y-%m-%d')} {element}: {input('Describe the change: ').strip()}"
    entry = f"    ('{title}', '{element}', [\n" + ''.join(f'        {s}\n' for s in steps) + '    ]),\n'
    source = open('element_migrations.py').read()
    assert source.count(MARKER) == 1
    with open('element_migrations.py', 'w') as f:
        f.write(source.replace(MARKER, entry + MARKER))
    print(f'\nAdded to element_migrations.py:\n{entry}')
    if by_hand:
        print('Replace the TODO, then run python3.12 migrations.py to see what it changes.')
        return
    importlib.reload(element_migrations)
    db = sqlite3.connect('l3d.db')
    show(run(db, [element_migrations.MIGRATIONS[-1]])[0])


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'pending'
    if command == 'new':
        new(*sys.argv[2:4])
    elif command == 'examples':
        from element_migrations import EXAMPLES
        db = sqlite3.connect('l3d.db')
        for entry in EXAMPLES:
            show(run(db, [entry])[0])
    else:
        db = sqlite3.connect('l3d.db')
        todo = pending(db)
        print(f'{len(todo)} migrations pending for l3d.db (dry run, nothing is written)')
        show(run(db, todo)[0])
