"""One-off migration: the numbered slot keys in the presets become names.

In a channel, 9 was the generator and 8 the colour. At the top of the state, 9
was the global channel. In 'context', channel 10 was a panel: index 0 the s2l
spectrum, index 1 the dashboard. Only channel and global presets carry these
keys; generator and effect presets are left untouched.

Safe to run more than once: a preset that is already migrated stays as it is.
Before changing anything it copies the database next to itself.

    python3.12 migrate_slot_keys.py [path/to/l3d.db]
"""
import json
import os
import shutil
import sqlite3
import sys

PANELS = {0: 's2l', 1: 'dashboard'}


def rename_slots(channel):
    """One channel's numbered generator and colour slots, as names."""
    if '9' in channel:
        channel['generator'] = channel.pop('9')
    if '8' in channel:
        channel['color'] = channel.pop('8')
    return channel


def rename_context(context):
    """MIDI context addresses, as names. Already named entries pass through."""
    renamed = []
    for section, slot in context:
        if section == 10:
            renamed.append(['panel', PANELS[slot]])
        elif section == 9:
            renamed.append(['global', slot])
        else:
            renamed.append([section, 'generator' if slot == 9 else slot])
    return renamed


def migrate_preset(kind, data):
    if kind == 'channel':
        return rename_slots(data)
    # a global preset is a whole state: the global channel, the channels, the context
    if '9' in data:
        data['global'] = rename_slots(data.pop('9'))
    for key in [k for k in data if k.isdigit()]:
        rename_slots(data[key])
    if 'context' in data:
        data['context'] = rename_context(data['context'])
    return data


def dump(data):
    # the same compact form db_manager.save_preset writes
    return json.dumps(data, indent=None, separators=(',', ':'))


def migrate(db_path='l3d.db'):
    backup = db_path + '.before-slot-keys'
    if not os.path.exists(backup):
        shutil.copy(db_path, backup)

    db = sqlite3.connect(db_path)
    rows = db.execute('''SELECT p.id, e.type, p.data FROM presets p
                         JOIN elements e ON e.id = p.element_id
                         WHERE e.type IN ('channel', 'global')''').fetchall()
    changed = 0
    for preset_id, kind, text in rows:
        before = dump(json.loads(text))
        after = dump(migrate_preset(kind, json.loads(text)))
        if after != before:
            db.execute('UPDATE presets SET data = ? WHERE id = ?', (after, preset_id))
            changed += 1
    db.commit()
    db.close()
    print(f'{changed} of {len(rows)} channel and global presets migrated (backup: {backup})')
    return changed


if __name__ == '__main__':
    migrate(sys.argv[1] if len(sys.argv) > 1 else 'l3d.db')
