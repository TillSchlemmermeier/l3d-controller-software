"""Smoke test for the core: state, renderer, MIDI, randomizer and API.

Drives the real code paths on a temporary copy of l3d.db, so the real database
is never touched. Run from core/ with the app stopped:

    python3.12 smoke_test.py

It checks that things work end to end, not how they look. Exit code is the
number of failed checks.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import multiprocessing as mp
import multiprocessing.shared_memory as shm

CORE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CORE)

# The state's slot vocabulary, in one place.
GENERATOR, COLOR, GLOBAL = 'generator', 'color', 'global'
S2L, DASHBOARD = ('panel', 's2l'), ('panel', 'dashboard')

results = []


def check(label, condition, detail=''):
    results.append(bool(condition))
    print(f"  {'PASS' if condition else 'FAIL'}  {label}{'' if condition else f'  -- {detail}'}")


def run(label, fn):
    """Run one check body; any exception is a failure, not a crash of the test."""
    try:
        fn()
    except Exception as e:
        check(label, False, f'{type(e).__name__}: {e}')


def quietly(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


for name in ('cube_data', 'global_s2l_memory'):
    if os.path.exists(f'/dev/shm/{name}'):
        sys.exit(f'shared memory {name!r} exists: stop the app before running the smoke test')

workdir = tempfile.mkdtemp(prefix='l3d_smoke_')
shutil.copy(os.path.join(CORE, 'l3d.db'), workdir)
os.chdir(workdir)          # DatabaseManager opens 'l3d.db' relative to the cwd

cube = shm.SharedMemory(create=True, name='cube_data', size=27000)
s2l = shm.SharedMemory(create=True, name='global_s2l_memory', size=512)
s2l.buf[:512] = bytes(512)

try:
    from UltraDict import UltraDict
    from fastapi.testclient import TestClient
    from managers.db_manager import DatabaseManager
    from managers.state_manager import StateManager
    from rendering_engine import rendering_engine
    from midi.translation import MidiTranslation
    from randomizer import Randomizer
    from server import WebSocketAPIServer, UDPBroadcastProtocol
    import routers.auth

    try:
        import migrate_slot_keys
        quietly(migrate_slot_keys.migrate, 'l3d.db')
    except ImportError:
        pass
    import migrations
    quietly(migrations.migrate, 'l3d.db')

    db = DatabaseManager()
    state = UltraDict({
        'IO': True, 'brightness': 1, 'fade': 0, 'autopilot': False, 'autopilot_time': 3,
        'random': 'all_elements', 's2l_values': [0.12, 0.2, 0.45, 0.7], 's2l_thresholds': [0, 0, 0, 0],
        's2l_normalize': False, 's2l_auto_normalize': True, 's2l_gain': 0.5, 's2l_update': True,
        'context': [[0, GENERATOR]] * 4, 'midi_update': 0, 'oneshot': 0, 'numberOfChannels': 0,
        GLOBAL: {'update': False, 'numberOfEffects': 0},
    }, recurse=False, name='l3d_smoke_state', buffer_size=1024 * 1024)
    sm = StateManager(state)

    # start from a real global preset that has channels and global effects
    candidates = []
    for name in (p['name'] for p in db.get_preset_names('global', 'presets')):
        data = db.get_preset('global', 'presets', name, False)
        if data.get('numberOfChannels', 0) >= 2 and data[GLOBAL].get('numberOfEffects', 0) >= 1:
            candidates.append(data)
    quietly(sm.load_global, candidates[0])
    engine = quietly(rendering_engine)

    def frames(n=5):
        for _ in range(n):
            quietly(engine.run, state)

    print('\nrender')
    run('frames from a loaded global preset', lambda: (frames(), check(
        'frames from a loaded global preset', engine.channelworld.any(), 'every channel rendered black')))
    run('update flags consumed', lambda: check('update flags consumed',
        not any(state[i][GENERATOR]['update'] for i in range(state['numberOfChannels'])),
        'a generator update flag is still set'))

    print('\napi')
    queue = mp.Queue()
    randomizer = quietly(Randomizer, state)
    threading.Thread(target=randomizer.run_autopilot_loop, args=(state, queue), daemon=True).start()
    server = quietly(WebSocketAPIServer, state, queue)
    routers.auth.ADMIN_TOKEN = 'smoke'
    client = TestClient(server.app)
    admin = {'X-Admin-Token': 'smoke'}

    def post(path, **kw):
        response = quietly(client.post, f'/api/{path}', **kw)
        check(f'POST {path}', response.status_code == 200, f'{response.status_code} {response.text[:120]}')
        return response

    generator = db.get_active_elements('generator')[0]['name']
    effect = db.get_active_elements('effect')[0]['name']
    ch_preset = db.get_preset_names('channel', 'presets')[0]['name']

    run('load', lambda: (
        post(f'load/generator/basic/0/0/{generator}'),
        post(f'load/effect/basic/0/0/{effect}'),
        post(f'load/effect/basic/{GLOBAL}/{state[GLOBAL]["numberOfEffects"]}/{effect}'),
        post(f'load/channel/{ch_preset}/1/0/presets'),
    ))
    run('generator landed', lambda: check('generator landed', state[0][GENERATOR]['name'] == generator,
                                         state[0][GENERATOR]['name']))

    color = {'gradient': [[0, '#ff0000'], [100, '#0000ff']], 'gradientType': 'linear', 'sectionWidth': 100,
             'sectionStart': 0, 'speed': 10, 'rotateSpeedY': 0, 'rotateSpeedZ': 0, 'soundToLightOptions': []}
    run('colour', lambda: (
        post(f'color-manager/{GLOBAL}', json=color),
        post('color-manager/0', json=color),
        check('global colour stored', state[GLOBAL][COLOR]['gradient'][0][1] == '#ff0000', state[GLOBAL].get(COLOR)),
        post('clear-gradient/0'),
        check('channel colour cleared', COLOR not in state[0], list(state[0])),
    ))

    def effect_moves():
        before = state[GLOBAL]['numberOfEffects']
        io_before = state[GLOBAL][0]['IO']
        post(f'toggleeffect/{GLOBAL}/0')
        check('global effect toggled', state[GLOBAL][0]['IO'] != io_before)
        post(f'copyeffect/0/0/{GLOBAL}/0')
        post(f'moveeffect/{GLOBAL}/0/1')
        check('effect copied into global', state[GLOBAL]['numberOfEffects'] == before + 1)
        quietly(client.delete, f'/api/remove/effect/{GLOBAL}/0')
        check('global effect removed', state[GLOBAL]['numberOfEffects'] == before)
    run('effect moves', effect_moves)

    def channel_moves():
        n = state['numberOfChannels']
        post('copychannel/0')
        post('movechannel/0/1')
        check('channel copied', state['numberOfChannels'] == n + 1)
        quietly(client.delete, f'/api/remove/channel/{n}/0')
        check('channel removed', state['numberOfChannels'] == n)
    run('channel moves', channel_moves)

    def select_every_kind():
        for section, slot in ((0, GENERATOR), (0, 0), (GLOBAL, 0), S2L, DASHBOARD):
            post(f'select/0/{section}/{slot}')
            check(f'context is {section}/{slot}', state['context'][0] == [section, slot], state['context'][0])
    run('select', select_every_kind)

    def effect_slot_past_the_end():
        # with numbered slots, effect index 8 used to overwrite the colour manager;
        # an index past the last effect would now leave a gap instead, so it's refused
        post('color-manager/0', json=color)
        count = state[0]['numberOfEffects']
        r = quietly(client.post, f'/api/load/effect/basic/0/8/{effect}')
        check('effect slot past the end refused', r.status_code == 422, r.status_code)
        check('colour and effects untouched', state[0][COLOR]['gradient'][0][1] == '#ff0000'
              and state[0]['numberOfEffects'] == count, state[0].get(COLOR))
    run('effect 8', effect_slot_past_the_end)

    def save_and_reload():
        for kind, channel, index in (('generator', 0, 0), ('effect', 0, 0), ('channel', 0, 0),
                                     ('global', 0, 0), ('effect', GLOBAL, 0)):
            data = {'preset': f'smoke_{kind}_{channel}', 'type': kind, 'channel': str(channel),
                    'index': str(index), 'force': 'true'}
            r = quietly(client.post, '/api/save/', data=data, headers=admin)
            check(f'save {kind} from {channel}/{index}', r.status_code == 200, f'{r.status_code} {r.text[:120]}')
        post('load/channel/smoke_channel_0/2/0/presets')
        check('channel preset round trip', state[2][GENERATOR]['name'] == state[0][GENERATOR]['name'])
        post('load/global/smoke_global_0/0/0/presets')
    run('save and reload', save_and_reload)

    def randomize_colour_via_queue():
        state[GLOBAL] = {**state[GLOBAL], COLOR: {**color, 'gradient': [[0, '#123456']], 'update': True}}
        post(f'randomize-color/{GLOBAL}')
        for _ in range(50):
            time.sleep(0.05)
            if state[GLOBAL].get(COLOR, {}).get('gradient') != [[0, '#123456']]:
                break
        check('randomizer recoloured the global channel',
              state[GLOBAL][COLOR]['gradient'] != [[0, '#123456']], 'global colour unchanged')
    run('randomize colour', randomize_colour_via_queue)

    print('\nmidi')
    midi = MidiTranslation(state)

    def fader(section, slot):
        sm.update_context(0, section, slot)
        target = state[section][slot]['params'][3]
        start = round(target * 127)
        quietly(midi.update_context, 0, 0, start)              # reach the stored value: pickup catches
        new = min(start + 5, 127) if start < 120 else start - 5
        quietly(midi.update_context, 0, 0, new)
        got = state[section][slot]['params'][3]
        check(f'fader drives {section}/{slot}', got == round(new / 127, 2), f'{got} != {round(new / 127, 2)}')
        check(f'fader readback {section}/{slot}', quietly(midi.get_context_midi_values)[0] == got)

    for section, slot in ((0, GENERATOR), (0, 0), (GLOBAL, 0)):
        run(f'fader {section}/{slot}', lambda s=section, e=slot: fader(s, e))

    def panels():
        sm.update_context(0, *S2L)
        quietly(midi.update_context, 0, 0, 100)
        check('fader drives the s2l panel', state['s2l_values'][0] == round(100 / 127, 2), state['s2l_values'])
        sm.update_context(0, *DASHBOARD)
        quietly(midi.update_context, 0, 4, 64)
        check('fader drives the dashboard panel', state['s2l_gain'] == round(64 / 127, 2), state['s2l_gain'])
        check('panel readback', len(quietly(midi.get_context_midi_values)) >= 4)
    run('panels', panels)

    def randomize_selected():
        sm.update_context(0, 0, GENERATOR)
        quietly(randomizer.trigger, 'selected_element')
        quietly(randomizer.trigger, 'random_channel_elements')
        quietly(randomizer.trigger, 'random_element')
        check('randomizer on selected and random elements', state[0][GENERATOR]['name'])
    run('randomize elements', randomize_selected)

    print('\nnotifications')

    def udp():
        calls = []

        class Recorder:
            def notify_frame_ready(self): pass
            async def update_element(self, *a): calls.append(a)
            async def update_key(self, *a): calls.append(a)
            async def update_state(self): calls.append(())

        async def go():
            p = UDPBroadcastProtocol(Recorder())
            p.datagram_received(f'update_element:{GLOBAL}:{COLOR}'.encode(), None)
            p.datagram_received(f'update_element:0:{GENERATOR}'.encode(), None)
            p.datagram_received(b'update_key:brightness:3', None)
            await asyncio.sleep(0.01)
        import asyncio
        asyncio.run(go())
        check('udp element addresses keep their keys',
              calls[:3] == [(GLOBAL, COLOR), (0, GENERATOR), ('brightness', 3)], calls)
    run('udp', udp)

    def broadcast_shape():
        sent = []

        class WS:
            async def send_json(self, m): sent.append(json.dumps(m))
        import asyncio
        server.connection_manager.active_websockets.append(WS())
        asyncio.run(server.connection_manager.update_element(GLOBAL, 0))
        asyncio.run(server.connection_manager.update_state())
        check('broadcasts are JSON', len(sent) == 2)
        server.connection_manager.active_websockets.clear()
    run('broadcast', broadcast_shape)

    print('\nrender after all of the above')
    run('frames after api, midi and randomizer', lambda: (frames(10), check(
        'frames after api, midi and randomizer', True)))

    state.unlink()
finally:
    cube.close(); cube.unlink()
    s2l.close(); s2l.unlink()
    shutil.rmtree(workdir, ignore_errors=True)

failed = results.count(False)
print(f'\n{len(results) - failed} passed, {failed} failed')
sys.exit(failed)
