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
- [Constraints & gotchas](#constraints--gotchas)
- [Security status](#security-status)
- [Roadmap / known issues](#roadmap--known-issues)

---

## Hardware

- **LED cube:** 10 stacked layers of 10×10 WS2811 LEDs (1000 pixels).
- **Driver:** an Arduino Due receives RGB frames over native USB serial and drives the LEDs with FastLED. Firmware is in [`Arduino/`](Arduino/).
- **Control surfaces:** MIDI controllers (Novation Launch Control, Midi Fighter, Launchpad) plus an on-screen touchscreen emulator. Real device drivers live in `core/midi_*.py`.
- **Host:** a Linux machine with a touchscreen, running the Electron app.

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
  Sound         PyAudio FFT → 6 doubles in global_s2l_memory shm (~100 Hz)
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
| UDP `127.0.0.1:8001` | Renderer → server "frame ready" trigger; sound → server spectrum JSON |
| WebSocket `:8000/ws` | State (JSON) + cube frames (binary) to the Electron UI and phones |
| Serial `/dev/ttyACM*` | RGB frames to the Arduino |

Saved data (elements, presets, gradients) lives in the SQLite database `core/l3d.db`, accessed via [`core/db_manager.py`](core/db_manager.py). The UltraDict is *runtime* state; the database is *persisted* state.

---

## The state model

The whole show is one **integer-keyed dictionary** (an `UltraDict` in shared memory). Understanding its shape is the key to understanding the app.

```
state = {
  "numberOfChannels": 1,
  "IO": false,          # master output on/off
  "brightness": 1.0,
  "fade": 0.0,
  "s2l_values": [...],  # sound-to-light band levels / config
  "context": [...],     # which MIDI context is focused
  "oneshot": 0,

  0: {                  # channel 0
    "IO": true, "brightness": 0.9, "fade": 0.0,
    9: { "name": "g_cube", "params": [...] },   # generator
    8: { "gradient": [...], ... },              # color manager
    "numberOfEffects": 0,
    # effects would be at keys 0, 1, 2, ...
  },
  # channels 1..7 follow the same shape

  9: { "numberOfEffects": 0 },  # the GLOBAL effects channel (applied after mixing)
}
```

Reserved keys inside a channel: **`9` = generator, `8` = color manager, `0..numberOfEffects-1` = effects**. At the top level, channel **`9` is the global effects channel**.

Each element carries `{"name", "update", "params"}`. `params` is a **positional array of 4-value groups** per parameter: `[label, variable_name, display value, midi value, ...]`. The live control value (0–1, set by MIDI) is every 4th entry — `params[3::4]` pulls them all out; the first three entries per group are display metadata written back by the element.

> **Note:** `UltraDict` is created with `recurse=False`, so nested edits don't auto-propagate. Code updates a channel by reassigning the whole sub-dict: `state[channel] = this_channel`.

---

## Elements: generators, effects, oneshots

Elements are the creative building blocks. There are three kinds, by directory and filename prefix:

- **Generators** — [`core/generators/g_*.py`](core/generators/) — produce a 3D image (a cube, sphere, wave, particle system…).
- **Effects** — [`core/effects/e_*.py`](core/effects/) — transform an image (rotation, blur, strobe, color fades, sound-reactive modulation…).
- **Oneshots** — [`core/oneshots/s_*.py`](core/oneshots/) — momentary triggered animations.

**Convention:** the class name equals the filename equals the registry key. `g_cube.py` contains `class g_cube`. This lowercase naming is intentional and load-bearing (the schema extractor and element registry rely on it).

Some heavy generators are written in **Fortran** and compiled with f2py for speed (spheres, torus, glow, and the `world2vox` voxel mapping). See the `.f90` files and the [`core/makefile`](core/makefile).

Element metadata (parameter names, ranges, categories) is extracted into [`core/element_schemas.json`](core/element_schemas.json) by the schema tooling (`schema_extractor.py` → `schema_comparator.py` → `schema_migrator.py`).

---

## Realtime data flow

**Rendering (25 FPS):** the renderer snapshots the state, and for each channel runs `generator → effects → color manager` to build a `[3,10,10,10]` RGB world. Channels are mixed (weighted by brightness), then global effects, color, fade and master brightness are applied. The final image is voxel-mapped through the Fortran `world2vox` routine, written to the Arduino over serial, and copied into the `cube_data` shared buffer. A UDP trigger tells the server a new frame is ready; the server broadcasts the latest frame to all connected screens/phones (coalescing bursts so slow clients can't back up the pipeline).

**Audio (sound-to-light):** the sound process continuously reads the microphone/line-in, runs an FFT, and reduces it to a few band levels plus a beat trigger. These are written as raw doubles into shared memory and read *directly* by sound-reactive elements every frame — the lowest-latency path in the system.

**MIDI:** turning a knob fires a callback that writes the corresponding parameter value straight into the state (with **soft-takeover** — a non-motorized fader won't jump the value until you sweep through the current position), then notifies the UI so on-screen controls update.

---

## Getting started

### Prerequisites

- **Python 3.12** available as `python3.12` on `PATH` (the Electron app spawns it directly — not a virtualenv).
- **Node.js** (for Vite / Electron).
- A C/Fortran toolchain with **`f2py3`** (from numpy) to build the native extensions.
- Linux (serial device paths and process management assume it).

### Build & run

```bash
# 1. Build the Fortran / f2py extensions (once; re-run after editing any .f90)
cd core
make                      # builds world2vox_fortran and friends

# 2. Install the Python dependencies for python3.12
pip install -r requirements.txt     # IMPORTANT: numpy stays <2 (see constraints)

# 3. Build the mobile app so the core can serve it to phones
cd ../mobile
npm install
npm run build

# 4. Install and run the desktop app
cd ..
npm install
npm run dev               # Vite dev server (frontend)
npm start                 # Electron — spawns the Python core automatically
```

To run the Python core on its own (without Electron):

```bash
cd core
python3.12 -u main.py            # normal start
python3.12 -u main.py --restore  # restore last state from state_backup.pkl
```

The API/WebSocket server listens on **`:8000`**; phones connect to `http://<host-ip>:8000` (the desktop app shows a QR code for this).

---

## Project layout

```
core/                Python realtime backend
  main.py            process launcher + shared-memory + state schema
  rendering_engine.py  the 25 FPS frame loop
  channel.py         per-channel generator→effects→color pipeline
  s2l_engine.py      audio capture + FFT (sound-to-light)
  midi_*.py          MIDI device drivers + on-screen emulator + translation
  server.py          FastAPI/uvicorn + WebSocket + UDP bridge
  connection_manager.py  WebSocket fan-out + frame broadcast
  state_manager.py   state mutation API
  db_manager.py      SQLite access (elements, presets, gradients)
  randomizer.py      autopilot / randomization
  routers/           HTTP endpoints (presets, state, gradients, system)
  generators/        g_*.py  (+ .f90 Fortran generators)
  effects/           e_*.py  (+ .f90 Fortran effects)
  oneshots/          s_*.py
  world2vox_*.f90    logical-image → physical-voxel mapping (Fortran)
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
   - `__init__(self)` — declare parameters.
   - `__call__(self, values)` for a generator (returns a `[3,10,10,10]` numpy array), or `__call__(self, world, values)` for an effect (transforms and returns the world).
   - `return_state(self)` — return display metadata for each parameter.
3. Register it in the database so it appears in the UI (via the admin tools / `db_manager`).
4. If it's performance-critical, consider a Fortran `.f90` + an f2py target in the `makefile`.

Keep everything **numpy 1.x compatible** (see below).

---
