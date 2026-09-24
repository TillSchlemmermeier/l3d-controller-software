"""Every change to a launched element's knobs, oldest first. See migrations.py.

Append only. An entry that has run somewhere is never edited or deleted: its
name is recorded in that database, so an edited version would never run there.
To correct one, add another entry. To undo one, restore the copy of the database
taken before it ran (l3d.db.before-<date>).

An entry is (name, element, steps). The name must be unique; the date keeps it
so. `python3.12 migrations.py new <element>` writes the entry from the diff of the
parameter block and asks what each change should do. `python3.12 migrations.py`
shows how many presets the pending entries change.

Steps, indices counting from 0, each seeing the knobs as the step before left them:
    keep(k, old=..., new=...)  store the value that makes the new line give what the old one gave
    change(k, fn)              store fn(stored value)
    derive(k, fn)              store fn(all stored values)
    insert(k, name, value)     a new knob; value may be fn(all stored values)
    remove(k)                  a knob is gone
    move(k, to)                a knob changes place

Changes that need no entry:
    - a knob renamed, a label or the displayed value changed: the element
      rewrites those itself when a preset loads.
    - a range changed and the presets should scale with it (same knob value,
      new meaning): the new line reads the old value.
    - drawing code in __call__: nothing stored depends on it. If it changes what a
      knob means (a constant like SIZE_BIGGEST), see the g_shapes example.
    - a new element: it has no old presets.

Not handled: renaming or deleting an element. Its presets name it and would be
orphaned, so launched elements keep their name.

keep() refuses an option that is no longer there, with the preset that holds
it, rather than guessing. Write the old line with its replacement instead (see
the e_mean example).
"""
import math
import numpy as np

from migrations import keep, change, derive, insert, remove, move

MIGRATIONS = [
    # new entries go above this line
]


# Never applied. One per kind of change, on real elements, so
# `python3.12 migrations.py examples` shows what each would do to the presets.
EXAMPLES = [
    # --- a knob's range or curve ---
    ('range grows, presets look the same', 'g_cube', [
        keep(0, old=lambda m: round(m*4), new=lambda m: round(m*8)),
    ]),
    ('range shrinks, values beyond it get the nearest one', 'g_cube_edges', [
        keep(0, old=lambda m: m*2 + 0.4, new=lambda m: m + 0.4),
    ]),
    ('range moves', 'e_bright_osci', [
        keep(1, old=lambda m: m*3+0.01, new=lambda m: m*3+0.5),
    ]),
    ('more whole-number steps', 'g_cube_edges', [
        keep(1, old=lambda m: int(3*m), new=lambda m: int(5*m)),
    ]),
    ('linear becomes a curve', 'g_torus', [
        keep(0, old=lambda m: m*8, new=lambda m: m**2*8),
    ]),
    ('truncation becomes rounding', 'g_cube', [
        keep(3, old=lambda m: 11 - int(m*10), new=lambda m: 11 - round(m*10)),
    ]),
    ('knob turned round', 'e_fade', [
        change(0, lambda m: 1 - m),
    ]),
    ('the range lives in a constant outside the block (SIZE_BIGGEST 4.7 -> 5.5)', 'g_shapes', [
        keep(1, old=lambda m: 1.5 + m*(4.7 - 1.5), new=lambda m: 1.5 + m*(5.5 - 1.5)),
    ]),

    # --- switches and options ---
    ('a switch flips above 0 instead of above 0.5', 'g_cube', [
        keep(1, old=lambda m: m > 0.5, new=lambda m: m > 0),
    ]),
    ('two-way mode: round() becomes the flip-above-0 convention', 'e_rare_strobo', [
        keep(3, old=lambda m: ['normal', 'invert'][round(m)], new=lambda m: ['normal', 'invert'][int(m > 0)]),
    ]),
    ('uneven s2l channel slices made even', 'g_cube', [
        keep(2, old=lambda m: ['noS2L', 0, 1, 2, 3, 'Trigger'][int(m*5)],
                new=lambda m: ['noS2L', 0, 1, 2, 3, 'Trigger'][min(int(m*6), 5)]),
    ]),
    ('an option added', 'g_planes', [
        keep(2, old=lambda m: ['cos', 'down', 'up'][round(m*2)], new=lambda m: ['cos', 'down', 'up', 'wave'][round(m*3)]),
    ]),
    ('options reordered', 'g_planes', [
        keep(1, old=lambda m: ['X', 'Y', 'Z'][int(round(m*2))], new=lambda m: ['Z', 'Y', 'X'][int(round(m*2))]),
    ]),
    ('options removed: up and down become vertical', 'e_mean', [
        # the old line, with each removed option replaced by what it becomes
        keep(1, old=lambda m: ['uniform', 'vertical', 'vertical', 'vertical'][int(m*3)],
                new=lambda m: ['uniform', 'vertical'][int(m > 0)]),
    ]),

    # --- knobs added, removed, moved ---
    ('a knob added at the end, off in old presets', 'e_fade', [
        insert(3, 'speed', 0.0),
    ]),
    ('a knob added in the middle', 'g_torus', [
        insert(2, 'wobble', 0.0),
    ]),
    ('one knob split in two: thickness becomes thickness and height', 'g_torus', [
        insert(2, 'height', lambda v: v[1]),
    ]),
    ('a knob removed', 'e_rare_strobo', [
        remove(2),
    ]),
    ('knobs reordered: the s2l channel moves to the end', 'e_strobe', [
        move(0, 5),
    ]),
    ('two knobs merged into one: speed goes, amount takes the larger', 'e_bright_osci', [
        derive(2, lambda v: max(v[0], v[2])),
        remove(0),
    ]),
    ('a knob that depends on another: iterations only count when inverted', 'e_strobe', [
        derive(5, lambda v: v[5] if v[4] > 0.5 else 0.0),
    ]),
    ('several changes at once: indices follow the steps before them', 'e_rare_strobo', [
        remove(2),                                                     # disp_prop goes, mode moves up to 2
        keep(2, old=lambda m: ['normal', 'invert'][round(m)], new=lambda m: ['normal', 'invert'][int(m > 0)]),
        insert(3, 'fade', 0.0),
    ]),
]
