# L3D Studio

A controller for a physical **LED cube** — designed for live music performance. L3D Studio runs fullscreen on a touchscreen, drives the cube's LEDs in real time, and lets you shape the visuals with **MIDI controllers** and **live audio** (sound-to-light). A phone can join over WiFi as a remote.

Visuals are composed from stackable building blocks: a **generator** creates a shape or motion, **effects** transform it, and a **color manager** paints it. Multiple such **channels** are mixed together into the final image sent to the cube.

---

## Table of contents

- [Hardware](#hardware)
- [Architecture](#architecture)
- [The state model](#the-state-model)
- [Elements: generators, effects, oneshots](#elements-generators-effects-oneshots)
- [Realtime data flow](#realtime-data-flow)
- [Getting started](#getting-started)
- [Project layout](#project-layout)
- [Adding a new generator or effect](#adding-a-new-generator-or-effect)
- [Changing an element's parameters](#changing-an-elements-parameters)

---

## Hardware

- **LED cube:** 10 stacked layers of 10×10 WS2811 LEDs (1000 pixels).
- **Driver:** an Arduino Due receives RGB frames over native USB serial and drives the LEDs with FastLED. Firmware is in [`Arduino/`](Arduino/).
- **Control surfaces:** MIDI controllers (Novation Launch Control, Midi Fighter, Launchpad) plus an on-screen touchscreen emulator. Real device drivers live in `core/midi/`.
- **Host:** a Linux machine with a touchscreen, running the Electron app. The UI is laid out for a 2560 px wide screen; on any other width Electron zooms the whole page to fit.

---

## Architecture

L3D Studio is three cooperating tiers:

1. **Electron shell** ([`electron/main.ts`](electron/main.ts)) — spawns the Python core, hosts the Vue UI, and bridges the core's WebSocket to the UI over IPC. Also reports the machine's LAN IP for the mobile QR code.
2. **Vue 3 frontend** ([`src/`](src/)) — the touchscreen UI (workbench, dashboard, previews, MIDI mapping). A separate lightweight web app in [`mobile/`](mobile/) is served to phones.
3. **Python core** ([`core/`](core/)) — all the realtime work, split across **six processes** that share memory.

```
                 Electron main (electron/main.ts)
                 ├─ spawns python3.12 core/main.py
                 └─ bridges ws://localhost:8000/ws ──IPC──► Vue renderer (src/)

core/main.py forks 6 processes, all sharing one UltraDict "state":

  Renderer      25 FPS loop → world2vox → serial to Arduino, + cube_data shm
  Sound         PyAudio FFT, 50 ms window every 16.7 ms → 6 doubles in global_s2l_memory shm
  MIDI          controller/emulator callbacks → param writes into state
  Server        FastAPI + uvicorn on :8000 — REST API + /ws + UDP bridge :8001
  Autopilot     timed preset randomization
  State Backup  pickles state → state_backup.pkl every 30 s
```

**Why six processes?** Python's GIL would serialize audio analysis, rendering, and networking if they were threads. Running them as separate processes lets them truly run in parallel; they coordinate through shared memory rather than message passing on the hot paths.

**Transports:**

| Channel | Purpose |
|---|---|
| UltraDict `state` | The live show state — single source of truth, guarded by `state.lock` |
| SharedMemory `cube_data` | 9×1000×3 `uint8` frame buffer (combined image + 8 per-channel previews) |
| SharedMemory `global_s2l_memory` | 6 doubles of audio analysis, read directly by effects |
| UDP `127.0.0.1:8001` | The other processes → server: "frame ready" from the renderer, "this changed, tell the UI" from MIDI and autopilot, spectrum JSON from sound |
| WebSocket `:8000/ws` | State (JSON) + cube frames (binary) to the Electron UI and phones |
| Serial `/dev/ttyACM*` | RGB frames to the Arduino |

Saved data (elements, presets, gradients) lives in the SQLite database `core/l3d.db`, accessed via [`core/managers/db_manager.py`](core/managers/db_manager.py). The UltraDict is *runtime* state; the database is *persisted* state.

---

## The state model

The whole show is one **dictionary** (an `UltraDict` in shared memory). Understanding its shape is the key to understanding the app. Keys are **numbers where there is a list to go through** (channels, effects) and **names everywhere else**.

```
state = {
  "IO": false,                      # master output on/off
  "brightness": 1.0,
  "fade": 0.0,
  "autopilot": false, "autopilot_time": 3, "random": "all_elements",
  "s2l_values": [...], "s2l_thresholds": [...], "s2l_gain": 0.5, ...   # sound-to-light settings
  "context": [[0, "generator"], [0, 0], [0, 0], [0, 0]],              # what the MIDI faders drive
  "oneshot": 0,
  "numberOfChannels": 1,

  0: {                              # channel 0
    "IO": true, "brightness": 0.9, "fade": 0.0,
    "generator": { "name": "g_cube", "update": true, "params": [...] },
    "color": { "gradient": [...], ... },     # the color manager, optional
    "numberOfEffects": 0,
    # effects at keys 0, 1, 2, ...
  },
  # channels 1..7 have the same shape

  "global": { "numberOfEffects": 0 },  # the global effects, applied after mixing; may carry a "color" too
}
```

Inside a channel: **`"generator"`**, **`"color"`** (optional) and the effects at **`0..numberOfEffects-1`**. At the top level, **`"global"`** is the global effects channel: effects and an optional color, no generator.

Each entry of `context` is an address: `[channel, slot]` for an element (`[0, "generator"]`, `[2, 1]` for effect 1 of channel 2, `["global", 0]`), or `["panel", "s2l" | "dashboard"]` for a panel. The API uses the same names in its URLs, e.g. `/api/select/0/global/2`.

Each element carries `{"name", "update", "params"}`. `params` is a **positional array of 4-value groups** per parameter: `[label, variable_name, display value, midi value, ...]`. The live control value (0–1, set by MIDI) is every 4th entry — `params[3::4]` pulls them all out; the first three entries per group are display metadata written back by the element.

> **Note:** `UltraDict` is created with `recurse=False`, so nested edits don't auto-propagate. Code updates a channel by reassigning the whole sub-dict: `state[channel] = this_channel`.

---

## Elements: generators, effects, oneshots

Elements are the creative building blocks. There are three kinds, by directory and filename prefix:

- **Generators** — [`core/generators/g_*.py`](core/generators/) — produce a 3D image (a cube, sphere, wave, particle system…).
- **Effects** — [`core/effects/e_*.py`](core/effects/) — transform an image (rotation, blur, strobe, color fades, sound-reactive modulation…).
- **Oneshots** — [`core/oneshots/s_*.py`](core/oneshots/) — momentary triggered animations.

**Convention:** the class name equals the filename equals the registry key. `g_cube.py` contains `class g_cube`. This lowercase naming is intentional and load-bearing (the element registry and the database rely on it).

Some heavy calculations are written in **Fortran** and compiled with f2py for speed (spheres, torus, glow, ellipsoid, outer shadow, and the `world2vox` voxel mapping). See the `.f90` files and the [`core/makefile`](core/makefile); `make` builds all of them.

---

## Realtime data flow

**Rendering (25 FPS):** the renderer snapshots the state, and for each channel runs `generator → effects → color manager` to build a `[3,10,10,10]` RGB world. Channels are mixed (weighted by brightness), then global effects, color, fade and master brightness are applied. The final image is voxel-mapped through the Fortran `world2vox` routine, written to the Arduino over serial, and copied into the `cube_data` shared buffer. A UDP trigger tells the server a new frame is ready; the server broadcasts the latest frame to all connected screens/phones (coalescing bursts so slow clients can't back up the pipeline).

**Audio (sound-to-light):** the sound process continuously reads the microphone/line-in, runs an FFT over the last 50 ms every 16.7 ms (60 times a second), and reduces it to a few band levels plus a beat trigger. These are written as raw doubles into shared memory and read *directly* by sound-reactive elements every frame — the lowest-latency path in the system.

**MIDI:** turning a knob fires a callback that writes the corresponding parameter value straight into the state (with **soft-takeover** — a non-motorized fader won't jump the value until you sweep through the current position), then notifies the UI so on-screen controls update.

---

## Getting started

### Prerequisites

- **Python 3.12** available as `python3.12` on `PATH` (the Electron app spawns it directly — not a virtualenv).
- **Node.js** (for Vite / Electron).
- **`gfortran`**, **`meson`** and **`ninja`** plus **`f2py3`** (from numpy) to build the native extensions. On Python 3.12, f2py builds with meson.
- Linux (serial device paths and process management assume it).

### Build & run

```bash
# 1. Build the Fortran / f2py extensions (once; re-run after editing any .f90)
cd core
make                      # builds world2vox_fortran and the other f2py modules

# 2. Install the Python dependencies for python3.12
pip install -r requirements.txt     # IMPORTANT: numpy stays <2 (see constraints)

# 3. Build the mobile app so the core can serve it to phones
cd ../mobile
npm install
npm run build

# 4. Install and run the desktop app
cd ..
npm install
npm run dev               # Vite dev server (frontend); npm run l3d is the same
npm start                 # Electron — spawns the Python core automatically
```

Starting the core also applies any pending preset migrations (see [Changing an element's parameters](#changing-an-elements-parameters)).

To run the Python core on its own (without Electron):

```bash
cd core
python3.12 -u main.py            # normal start
python3.12 -u main.py --restore  # restore last state from state_backup.pkl
```

The API/WebSocket server listens on **`:8000`**; phones connect to `http://<host-ip>:8000` (the desktop app shows a QR code for this).

### Smoke test

With the app stopped, `cd core && python3.12 smoke_test.py` drives state, renderer, MIDI, randomizer and the API end to end on a temporary copy of the database. The exit code is the number of failed checks. Run it after changes to the state shape, the API or the MIDI path.

---

## Project layout

```
core/                Python realtime backend
  main.py            process launcher + shared memory + default state; applies migrations at startup
  rendering_engine.py  the 25 FPS frame loop
  channel.py         per-channel generator→effects→color pipeline
  s2l_engine.py      audio capture + FFT (sound-to-light)
  midi/              MIDI device drivers + on-screen emulator + translation
  server.py          FastAPI/uvicorn + WebSocket + UDP bridge
  managers/          connection_manager (WebSocket fan-out + frame broadcast),
                     state_manager (state mutation API),
                     db_manager (SQLite: elements, presets, gradients)
  randomizer.py      autopilot / randomization
  element_registry.py  creates elements by name (whitelisted)
  migrations.py      preset migration tool; element_migrations.py holds the entries
  migrate_slot_keys.py  one-off conversion of databases from before the named slots
  smoke_test.py      end-to-end check on a copy of the database
  routes.py          every HTTP endpoint (presets, live state, gradients, system)
  generators/        g_*.py  (+ .f90 Fortran generators)
  effects/           e_*.py  (+ .f90 Fortran effects)
  oneshots/          s_*.py
  world2vox_revis.f90  logical-image → physical-voxel mapping (Fortran)
  makefile           builds the f2py modules
  l3d.db             SQLite database
electron/            Electron main process + preload
src/                 Vue 3 + TypeScript + Tailwind touchscreen UI
mobile/              Separate lightweight web app served to phones
Arduino/             LED cube firmware (FastLED)
```

---

## Adding a new generator or effect

1. Create `core/generators/g_myshape.py` (or `core/effects/e_myeffect.py`). The **class name must match the filename**: `class g_myshape`.
2. Implement the element interface:
   - `__init__(self)` — set the defaults.
   - `__call__(self, values)` for a generator (returns a `[3,10,10,10]` numpy array), or `__call__(self, world, values)` for an effect (transforms and returns the world).
   - `return_state(self)` — return display metadata for each parameter.
   - Read the knobs between `# === PARAMETERS START ===` and `# === PARAMETERS END ===`, one per line (`self.x = <expression of args[k]>`), so the migration tool can read them later.
3. Register it in the database so it appears in the UI (via the admin tools / `managers/db_manager.py`).
4. If it's performance-critical, consider a Fortran `.f90` + an f2py target in the `makefile`.

Keep everything **numpy 1.x compatible** (see below).

---

## Changing an element's parameters

A preset stores each knob only as a 0–1 value, in order. When a line in an element's parameter block changes (a range, a curve, a mode list, a knob added, removed or moved), every stored value would silently start meaning something else. So each such change gets a short entry in `core/element_migrations.py` that says what should happen to the stored values. The most common entry is `keep(...)`: store the value that makes the new line give the same result as the old one, so existing presets look exactly as before. Renaming a knob, changing a label or the drawing code, and adding a new element need no entry.

```bash
cd core
python3.12 migrations.py new g_cube   # before committing: diff the parameter block against the last commit,
                                      # answer what each change should do, the entry is written for you
python3.12 migrations.py              # dry run: how many presets the pending entries change
python3.12 migrations.py examples     # the same for an example of every kind of change
```

Starting the core applies the entries this database hasn't had yet: to the element's own presets, to the copies inside channel and global presets, and to `state_backup.pkl`. The database is copied to `l3d.db.before-<date>` first, and every applied entry is recorded in its `migrations` table. So every database (the development one, the show machine's) gets each change exactly once, the first time it runs the new code.

The file is append-only: never edit or delete an entry that may have run somewhere. To correct a mistake, add a new entry; to undo one, restore the database copy. Parameter lines must be self-contained (`self.x = <expression of args[k]>`, with numbers and lists written out), because the tool reads them as code.

---
